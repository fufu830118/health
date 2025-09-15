# 🏥 健康活動問答系統

一個基於Flask的中文健康教育問答應用，具有響應式設計、音效系統和倒數計時功能。

## ✨ 主要功能

- 📊 **Excel問題庫管理** - 從Excel檔案載入分類問題
- 🎵 **純JavaScript音效系統** - 使用Web Audio API生成音效
- ⏰ **倒數計時器** - 30秒答題時間限制，帶音效提醒
- 📱 **響應式設計** - 適配手機、平板、桌面等各種設備
- 🎨 **現代化UI** - 使用Tailwind CSS和自定義動畫效果
- 🔄 **問題隨機化** - 避免重複，增加答題趣味性

## 🚀 快速開始

### 安裝依賴

```bash
# 創建虛擬環境
python -m venv venv

# 激活虛擬環境 (Windows)
venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt
```

### 啟動應用

**方式1：使用批次檔（推薦）**
```bash
# 雙擊運行
start_health_quiz.bat
```

**方式2：命令行啟動**
```bash
python app.py
```

### 訪問應用

打開瀏覽器訪問：http://127.0.0.1:5000

## 📁 檔案結構

```
health-quiz/
├── app.py                      # Flask主應用程式
├── requirements.txt            # Python依賴清單
├── index.html                  # 主選單頁面
├── question_display.html       # 問題顯示頁面
├── feedback_correct.html       # 正確答案回饋
├── feedback_incorrect.html     # 錯誤答案回饋
├── timeout_feedback.html       # 超時回饋頁面
├── start_health_quiz.bat      # Windows啟動腳本
├── 問答題庫範本.xlsx           # Excel問題資料庫
├── CLAUDE.md                  # 專案文檔
└── README.md                  # 本文件
```

## 🎼 音效系統

本系統使用**Web Audio API**純JavaScript實時生成音效，無需外部音頻檔案：

- **Tick音效**：1200Hz方波，用於倒數計時（10-1秒）
- **Timeout音效**：300+200+150Hz和弦，時間到警報
- **互動音效**：按鈕懸停、點擊、選擇等音效回饋

## 📊 問題資料格式

Excel檔案應包含以下欄位：
- `類別` - 問題分類
- `題目內容` - 問題文字
- `選項A` - 第一個選項
- `選項B` - 第二個選項  
- `選項C` - 第三個選項
- `正確答案` - A、B或C

## 🛠️ 技術棧

- **後端**：Flask 2.3.2
- **前端**：HTML5 + CSS3 + Vanilla JavaScript
- **樣式**：Tailwind CSS + 自定義CSS
- **圖標**：Font Awesome 6
- **數據處理**：Pandas + openpyxl
- **音效**：Web Audio API

## 📱 響應式設計

- **桌面**：完整功能，大字體顯示
- **平板**：適中尺寸，觸控優化
- **手機**：緊湊佈局，大按鈕設計

## 🎨 設計特色

- **現代漸變背景**
- **毛玻璃效果容器**
- **流暢的動畫過渡**
- **3D按鈕懸浮效果**
- **智能倒數計時視覺提示**

## 📝 開發說明

- 所有HTML模板位於根目錄
- 使用Flask session管理問題狀態
- 支持PyInstaller打包為獨立執行檔
- 音效系統自動適配瀏覽器支持

## 📄 授權

MIT License

---

🎉 **享受您的健康問答之旅！**