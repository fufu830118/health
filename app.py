from flask import Flask, jsonify, request, render_template, session, send_from_directory
import pandas as pd
import os
import random
import sys
import threading
import webbrowser
import tkinter as tk
from tkinter import messagebox
import secrets
from threading import Lock

# 建立 Flask app
if getattr(sys, 'frozen', False):
    template_dir = os.path.join(sys._MEIPASS)
    video_dir = os.path.join(sys._MEIPASS, '影片')
    audio_dir = os.path.join(sys._MEIPASS, '音效')
else:
    template_dir = os.path.dirname(os.path.abspath(__file__))
    video_dir = os.path.join(template_dir, '影片')
    audio_dir = os.path.join(template_dir, '音效')

app = Flask(__name__, template_folder=template_dir)

# 安全的 secret_key 生成：從環境變數讀取，若無則生成隨機值
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or secrets.token_hex(32)

# Excel 檔案鎖定保護（防止並發寫入衝突）
excel_lock = Lock()

# 允許的影片副檔名（安全白名單）
ALLOWED_VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.wmv', '.jpg', '.jpeg', '.png', '.gif'}

# 允許的音效副檔名（安全白名單）
ALLOWED_AUDIO_EXTENSIONS = {'.mp3', '.wav', '.ogg', '.m4a'}

def load_questions():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(application_path, "問答題庫範本.xlsx")

    try:
        print(f"Attempting to load questions from: {file_path}")
        df = pd.read_excel(file_path)
        categorized_questions = {}
        for index, row in df.iterrows():
            category = row["類別"]
            if category not in categorized_questions:
                categorized_questions[category] = []
            question_data = {
                "question": row["題目內容"],
                "options": [row["選項A"], row["選項B"], row["選項C"]],
                "answer": row["正確答案"],
                "category": category,
                "excel_index": index  # 新增：記錄Excel中的索引位置
            }
            categorized_questions[category].append(question_data)
        print(f"Successfully loaded {sum(len(v) for v in categorized_questions.values())} questions.")
        return categorized_questions, file_path
    except Exception as e:
        print(f"[ERROR] {e}")
        messagebox.showerror("錯誤", f"無法載入題庫: {e}")
        sys.exit(1)

def mark_question_as_used(file_path, excel_index):
    """在Excel中標記題目已被使用（使用檔案鎖定防止並發問題）"""
    with excel_lock:
        try:
            df = pd.read_excel(file_path)
            df.at[excel_index, '出現過'] = '是'
            df.to_excel(file_path, index=False)
            print(f"Marked question at index {excel_index} as used")
        except Exception as e:
            print(f"Error marking question as used: {e}")

def reset_category_marks(file_path, category):
    """重置某個類別的所有標記（使用檔案鎖定防止並發問題）"""
    with excel_lock:
        try:
            df = pd.read_excel(file_path)
            category_mask = df['類別'] == category
            df.loc[category_mask, '出現過'] = None
            df.to_excel(file_path, index=False)
            print(f"Reset all marks for category: {category}")
        except Exception as e:
            print(f"Error resetting category marks: {e}")

all_categorized_questions, excel_file_path = load_questions()

correct_messages = [
    "太好了，恭喜您，答對了！🎉",
    "很棒喔～這題答得很精準！",
    "答對了！繼續加油！",
    "太好了，您真是小天才！",
    "回答正確，讚啦！👍",
    "完全沒難倒您呢！"
]

incorrect_messages = [
    "可惜了，再接再厲唷！",
    "答錯了～下次會更好！",
    "沒關係，下一題一定可以！",
    "差一點點而已，加油 💪",
    "這題真的不簡單，下次注意！"
]

def load_questions_fresh_from_excel(category):
    """直接從Excel重新載入指定類別的題目，獲取最新的'出現過'狀態（使用檔案鎖定）"""
    with excel_lock:
        try:
            df = pd.read_excel(excel_file_path)

            # 確保'出現過'欄位存在
            if '出現過' not in df.columns:
                df['出現過'] = ''

            questions = []
            category_questions = df[df['類別'] == category]

            for index, row in category_questions.iterrows():
                question_data = {
                    "category": row['類別'],
                    "question": row['題目內容'],
                    "options": [row['選項A'], row['選項B'], row['選項C']],
                    "correct_answer": row['正確答案'],
                    "appeared": row['出現過'] == '是',
                    "excel_index": index
                }
                questions.append(question_data)

            return questions
        except Exception as e:
            print(f"重新載入題目時發生錯誤: {e}")
            return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/question_display')
def question_display():
    return render_template('question_display.html')

@app.route('/feedback_correct')
def feedback_correct():
    return render_template('feedback_correct.html')

@app.route('/feedback_incorrect')
def feedback_incorrect():
    return render_template('feedback_incorrect.html')

@app.route('/timeout_feedback')
def timeout_feedback():
    return render_template('timeout_feedback.html')

@app.route('/no_more_questions')
def no_more_questions():
    return render_template('no_more_questions.html')

@app.route('/punishment_videos')
def punishment_videos():
    return render_template('punishment_videos.html')

@app.route('/videos/<path:filename>')
def serve_video(filename):
    """提供影片和圖片檔案服務（支援中文檔名，防止路徑遍歷攻擊）"""
    try:
        # 防止路徑遍歷：移除危險字元但保留中文
        # 禁止: ../ .\ 絕對路徑 等危險模式
        if '..' in filename or '\\' in filename or filename.startswith('/'):
            return jsonify({"error": "Invalid filename"}), 403

        # 只允許檔名，不允許路徑分隔符
        if os.path.sep in filename or (os.path.altsep and os.path.altsep in filename):
            return jsonify({"error": "Invalid filename"}), 403

        # 檢查副檔名白名單
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in ALLOWED_VIDEO_EXTENSIONS:
            return jsonify({"error": "File type not allowed"}), 403

        # 建構完整路徑並驗證
        file_path = os.path.join(video_dir, filename)
        file_path = os.path.abspath(file_path)

        # 確保檔案在指定目錄內（防止路徑遍歷）
        if not file_path.startswith(os.path.abspath(video_dir)):
            return jsonify({"error": "Access denied"}), 403

        # 檢查檔案是否存在
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404

        return send_from_directory(video_dir, filename)
    except Exception as e:
        print(f"Error serving video file: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    """提供音效檔案服務（支援中文檔名，防止路徑遍歷攻擊）"""
    try:
        # 防止路徑遍歷
        if '..' in filename or '\\' in filename or filename.startswith('/'):
            return jsonify({"error": "Invalid filename"}), 403

        # 只允許檔名，不允許路徑分隔符
        if os.path.sep in filename or (os.path.altsep and os.path.altsep in filename):
            return jsonify({"error": "Invalid filename"}), 403

        # 檢查副檔名白名單
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in ALLOWED_AUDIO_EXTENSIONS:
            return jsonify({"error": "File type not allowed"}), 403

        # 建構完整路徑並驗證
        file_path = os.path.join(audio_dir, filename)
        file_path = os.path.abspath(file_path)

        # 確保檔案在指定目錄內
        if not file_path.startswith(os.path.abspath(audio_dir)):
            return jsonify({"error": "Access denied"}), 403

        # 檢查檔案是否存在
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404

        return send_from_directory(audio_dir, filename)
    except Exception as e:
        print(f"Error serving audio file: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/clear_session', methods=['POST'])
def clear_session():
    """清除session中的已問題目記錄，讓題目可以重新開始"""
    try:
        if 'asked_questions' in session:
            session.pop('asked_questions', None)
            session.modified = True
        return jsonify({
            "success": True,
            "message": "Session已清除，可以重新開始答題"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"清除session失敗: {str(e)}"
        })

@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify(list(all_categorized_questions.keys()))

@app.route('/api/questions', methods=['GET'])
def get_questions():
    category = request.args.get('category')

    # 輸入驗證：類別名稱
    if not category or not isinstance(category, str):
        return jsonify({"error": "Invalid category parameter"}), 400

    if category not in all_categorized_questions:
        return jsonify({"error": "Category not found"}), 404

    # 重新載入Excel檢查最新的"出現過"狀態
    fresh_questions = load_questions_fresh_from_excel(category)

    # 找出未出現過的題目
    available_questions = [q for q in fresh_questions if not q.get('appeared', False)]

    # 如果該類別沒有可用題目
    if not available_questions:
        return jsonify({
            "no_more_questions": True,
            "message": "此類別所有題目已完成",
            "redirect_url": "/no_more_questions"
        })

    # 隨機選擇一個題目
    question_data = random.choice(available_questions)

    # 標記題目為已使用
    mark_question_as_used(excel_file_path, question_data["excel_index"])

    return jsonify({
        "question": question_data["question"],
        "options": question_data["options"],
        "category": question_data["category"],
        "question_index": question_data["excel_index"],
        "image_url": question_data.get("image_url", ""),
        "progress": {
            "current": len([q for q in fresh_questions if q.get('appeared', False)]) + 1,
            "total": len(fresh_questions)
        }
    })

@app.route('/api/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()

    # 輸入驗證
    if not data:
        return jsonify({"error": "No data provided"}), 400

    excel_index = data.get('question_index')
    selected_option = data.get('selected_option')
    category = data.get('category')

    # 必填欄位驗證
    if excel_index is None or selected_option is None or category is None:
        return jsonify({"error": "Missing required fields"}), 400

    # 資料型態驗證
    if not isinstance(excel_index, int) or excel_index < 0:
        return jsonify({"error": "Invalid question_index"}), 400

    if not isinstance(selected_option, str) or not selected_option.strip():
        return jsonify({"error": "Invalid selected_option"}), 400

    if not isinstance(category, str) or category not in all_categorized_questions:
        return jsonify({"error": "Invalid category"}), 400

    try:
        # 直接從Excel獲取題目資料（使用檔案鎖定）
        with excel_lock:
            df = pd.read_excel(excel_file_path)

            # 檢查索引範圍
            if excel_index >= len(df):
                return jsonify({"error": "Question index out of range"}), 400

            question_row = df.iloc[excel_index]

        # 檢查題目是否屬於指定類別
        if question_row['類別'] != category:
            return jsonify({"error": "Question category mismatch"}), 400

        # 獲取選項
        options = [question_row['選項A'], question_row['選項B'], question_row['選項C']]
        correct_answer = question_row['正確答案']

        # 找出選中選項的索引
        selected_option_index = -1
        for i, option_text in enumerate(options):
            if selected_option == option_text:
                selected_option_index = i
                break

        if selected_option_index == -1:
            return jsonify({"error": "Invalid selected option"}), 400

        # 將索引轉換為字母（A, B, C）
        selected_option_letter = chr(ord('A') + selected_option_index)
        is_correct = (selected_option_letter == correct_answer)

        feedback = random.choice(correct_messages) if is_correct else random.choice(incorrect_messages)
        redirect_url = '/feedback_correct' if is_correct else '/feedback_incorrect'

        return jsonify({
            "is_correct": is_correct,
            "feedback": feedback,
            "correct_answer": correct_answer,
            "redirect_url": redirect_url
        })
    except Exception as e:
        print(f"檢查答案時發生錯誤: {e}")
        return jsonify({"error": "Internal server error"}), 500

def start_server():
    app.run(port=5000, debug=True)

def create_ui():
    root = tk.Tk()
    root.title("健康活動問答啟動器")
    root.geometry("400x200")

    status_label = tk.Label(root, text="伺服器啟動中，請稍候...")
    status_label.pack(pady=20)

    start_button = tk.Button(root, text="開始活動", state=tk.DISABLED, command=lambda: webbrowser.open("http://127.0.0.1:5000/"))
    start_button.pack(pady=10)

    exit_button = tk.Button(root, text="離開", command=lambda: root.destroy())
    exit_button.pack(pady=10)

    def server_thread():
        server = threading.Thread(target=start_server, daemon=True)
        server.start()
        # 模擬啟動時間（你可以用真實檢查機制替代）
        root.after(2000, lambda: enable_start(status_label, start_button))

    def enable_start(label, button):
        label.config(text="伺服器啟動完成，您可以點選『開始活動』")
        button.config(state=tk.NORMAL)

    server_thread()
    root.mainloop()

if __name__ == '__main__':
    # Console startup mode
    print("="*60)
    print("健康活動問答系統 - 控制台版本")
    print("="*60)
    print("正在啟動Flask服務器...")

    # 從環境變數判斷是否為生產環境
    is_production = os.environ.get('FLASK_ENV') == 'production'

    print("\\n服務器資訊:")
    print("   URL: http://127.0.0.1:5000")
    print(f"   環境: {'生產模式' if is_production else '開發模式'}")
    print("\\n使用說明:")
    print("   1. 服務器啟動後，在瀏覽器中訪問 http://127.0.0.1:5000")
    print("   2. 選擇問題類別開始答題")
    print("   3. 按 Ctrl+C 停止服務器")
    print("\\n" + "="*60)
    print("服務器正在啟動中...")
    print("="*60)

    try:
        # 只在開發環境啟用 debug 模式
        app.run(host='127.0.0.1', port=5000, debug=not is_production)
    except KeyboardInterrupt:
        print("\\n\\n服務器已停止")
        print("感謝使用健康活動問答系統！")
