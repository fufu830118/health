# CLAUDE.md

本檔案為 Claude Code (claude.ai/code) 提供此專案的開發指引。

## 專案概述

這是一個現代化的中文健康教育問答應用，使用 Flask 後端和先進的 HTML/CSS/JavaScript 前端技術。主要特色包括：未來感玻璃擬物化 UI、Web Audio API 音效系統、Excel 整合問題管理，以及運動懲罰影片展示系統。

## 架構說明

### 後端架構
- **Flask 應用** (`app.py`): 主伺服器，提供 REST API 端點，支援控制台啟動模式
- **Excel 問題管理系統**:
  - 從 `問答題庫範本.xlsx` 載入，欄位包含：題號、類別、題目內容、選項A/B/C、正確答案、詳解、出現過
  - 共 50 題，平均分布於 5 個類別（每類別 10 題）
  - 使用 `出現過` 欄位追蹤已使用題目，避免重複出題
  - 即時更新 Excel 標記已使用題目
  - 類別題目全部答完時自動重置標記
  - 使用 `threading.Lock` 防止並發寫入衝突
- **靜態檔案服務**:
  - 影片/圖片檔案透過 `/videos/<filename>` 路由從 `影片/` 目錄提供
  - 音效檔案透過 `/audio/<filename>` 路由從 `音效/` 目錄提供
  - 具備路徑遍歷攻擊防護和檔案類型白名單驗證

### 問題類別（固定 5 個）
應用支援精確 5 個問題類別，每類別 10 題：
1. **環保題** - `fas fa-recycle` 圖示
2. **安全題** - `fas fa-shield-alt` 圖示
3. **衛生題** - `fas fa-hands-wash` 圖示
4. **健康題** - `fas fa-heartbeat` 圖示
5. **防災題** - `fas fa-exclamation-triangle` 圖示

### 前端架構
- **未來感主選單** (`index.html`):
  - 玻璃擬物化設計配合動態粒子背景
  - 從 API 動態載入類別，搭配自訂 FontAwesome 圖示
  - 「運動懲罰示範」按鈕連結至影片展示頁
  - CSS Grid 響應式佈局與懸停動畫
  - 現代漸層文字特效與發光動畫

- **運動懲罰影片展示** (`punishment_videos.html`):
  - **完整中文註解**：每一行都有詳細中文說明
  - 網格佈局顯示 8 個運動影片/圖片（從 `影片/` 資料夾）
  - 模態視窗全螢幕影片播放
  - 支援 MP4 影片和 JPG 圖片
  - 自動產生縮圖與播放/圖片圖示
  - 點擊播放，ESC 或背景點擊關閉

- **進階問題顯示** (`question_display.html`):
  - 30 秒倒數計時器，視覺警告（10 秒黃色、5 秒紅色）
  - Web Audio API 音效系統，無需外部音效檔案即時生成音調
  - 玻璃擬物化按鈕互動選項選擇
  - 即時視覺回饋與動畫

- **增強回饋系統**:
  - `feedback_correct.html` - 答對回饋與動畫
  - `feedback_incorrect.html` - 答錯回饋，包含詳解顯示（從 Excel `詳解` 欄位）
  - `timeout_feedback.html` - 逾時處理
  - `no_more_questions.html` - 類別完成通知

### 現代化 UI 特色
- **玻璃擬物化設計**: 背景模糊效果配合半透明容器
- **動態粒子背景**: 純 CSS 動畫浮動粒子效果
- **Web Audio API 音效系統**:
  - 即時音調生成（無需外部音效檔案）
  - 情境音效（tick、warning、success、error）
  - 用戶互動觸發音效上下文初始化
- **進階響應式設計**: Mobile-first 設計搭配 Tailwind CSS
- **流暢動畫**: CSS 過渡、變形和關鍵影格動畫

## API 端點

- `GET /` - 主選單頁面
- `GET /question_display` - 問題顯示頁面
- `GET /punishment_videos` - 運動懲罰影片展示頁面
- `GET /videos/<filename>` - 從 `影片/` 目錄提供影片/圖片檔案
- `GET /audio/<filename>` - 從 `音效/` 目錄提供音效檔案
- `GET /api/categories` - 返回 5 個問題類別的陣列（從 Excel 載入）
- `GET /api/questions?category={category}` - 返回指定類別的隨機未使用問題
- `POST /api/check_answer` - 驗證答案並返回回饋與重定向 URL（包含詳解）
- `POST /api/clear_session` - 清除 session 資料（舊版支援）

## 常用開發指令

### 執行應用程式
```bash
# 啟動虛擬環境
venv\Scripts\activate  # Windows

# 安裝相依套件（首次執行）
pip install -r requirements.txt

# 執行 Flask 應用（控制台模式 - 建議）
python app.py

# 瀏覽器存取：http://127.0.0.1:5000
# 伺服器執行於 port 5000，開發模式（除非設定 FLASK_ENV=production）
```

### Windows 快速啟動
```bash
# 使用批次檔一鍵啟動
start_health_quiz.bat

# 批次檔會：
# 1. 檢查虛擬環境是否存在
# 2. 啟動 Flask 應用
# 3. 顯示伺服器資訊
```

### 修改後重新啟動
修改 Excel 資料或 Python 程式碼後：
1. 停止伺服器（在終端機按 Ctrl+C）
2. 重新執行 `python app.py`
3. 重新整理瀏覽器查看變更

**注意**: Excel 變更需要重啟伺服器，因為資料在啟動時載入（`app.py` 第 92 行的 `load_questions()`）。

### 重置問題標記
若要重置某類別的「出現過」標記：
```python
# 在 Python console 或修改 app.py
reset_category_marks(excel_file_path, "健康題")
```

## 檔案結構

### 核心應用檔案
- `app.py` - Flask 應用，包含影片/音效服務路由
- `requirements.txt` - Python 相依套件（Flask 2.3.2, openpyxl）
- `問答題庫範本.xlsx` - Excel 問題資料庫（50 題，5 類別）
- `影片/` - 運動影片和圖片目錄（8 個檔案）
- `音效/` - 音效檔案目錄（選用，Web Audio API 可無檔案運作）
- `start_health_quiz.bat` - Windows 快速啟動批次檔

### HTML 範本
所有 HTML 檔案使用：
- **Tailwind CSS** via CDN - 實用優先樣式框架
- **FontAwesome 6** - 現代化圖示庫
- **微軟正黑體** - 中文文字渲染
- **深色主題**: 未來感配色，青色/紫色/粉色/紅色強調色
- **玻璃擬物化效果**: 背景模糊濾鏡與透明設計
- **CSS 自訂屬性**: 在 `:root` 中集中主題設定

### 樣式架構
- **CSS 變數**: 在 `:root` 選擇器中集中定義
  - `--primary-bg`, `--secondary-bg`, `--accent-cyan`, `--accent-purple`, `--accent-pink`, `--accent-red`
  - `--text-primary`, `--text-secondary`, `--glass-bg`
- **響應式斷點**: 768px（平板）、480px（手機）
- **動畫系統**: 基於關鍵影格的懸停效果與過渡
- **元件化樣式**: 可重用的 `.category-button`、`.glass-container`、`.video-card` 類別

## 應用流程

1. **啟動**: 控制台模式，Flask 開發伺服器執行於 port 5000
2. **主選單**: 5 個類別按鈕 + 1 個運動影片展示按鈕
3. **類別選擇**: 點擊類別開始問答 或 點擊運動按鈕觀看影片
4. **問題顯示**: 隨機未使用問題，配合 30 秒動畫倒數計時
5. **音效回饋**: Web Audio API 提供情境音效
6. **提交答案**: 即時回饋與動畫過渡，顯示詳解（如有）
7. **進度追蹤**: Excel 使用狀態追蹤防止重複
8. **類別完成**: 類別 10 題全部回答後自動重定向

## 技術實作細節

### 音效系統架構
- **Web Audio API**: 純 JavaScript 音調生成
- **音效類型**: click、hover、tick、warning、critical、timeout、success、error
- **上下文管理**: 用戶觸發音效上下文，符合瀏覽器相容性
- **漸進增強**: 音效無法使用時優雅降級

### Excel 整合
- **openpyxl 函式庫**: 直接操作 Excel 檔案
- **即時更新**: 透過 `mark_question_as_used()` 函式標記已使用問題
- **基於類別載入**: `load_questions_fresh_from_excel()` 讀取最新狀態
- **錯誤處理**: 遺失欄位或資料時的優雅降級
- **並發控制**: 使用 `threading.Lock` 防止多執行緒寫入衝突

### 影片展示系統
- **靜態檔案服務**: Flask `send_from_directory()` 從 `影片/` 資料夾提供檔案
- **模態系統**: 全螢幕覆蓋層影片播放
- **響應式網格**: CSS Grid 使用 `repeat(auto-fill, minmax(320px, 1fr))`
- **媒體偵測**: 自動處理影片和圖片檔案類型
- **事件處理**: 點擊、ESC 鍵、背景點擊關閉模態視窗

### 安全性機制
- **路徑遍歷防護**: 檢查 `..`、`\`、絕對路徑等危險字元
- **檔案類型白名單**:
  - 影片：`.mp4`, `.avi`, `.mov`, `.wmv`, `.jpg`, `.jpeg`, `.png`, `.gif`
  - 音效：`.mp3`, `.wav`, `.ogg`, `.m4a`
- **路徑驗證**: 使用 `os.path.abspath()` 確保檔案在允許目錄內
- **輸入驗證**: API 端點驗證所有輸入參數類型和範圍

### 響應式設計策略
- **Mobile-First**: 基礎樣式針對行動裝置優化
- **漸進增強**: 透過媒體查詢新增桌面功能
- **觸控友善**: 行動裝置上的大型按鈕和觸控目標
- **效能優化**: 優化動畫和過渡效果

## 開發注意事項

### 新增問題類別
**重要**: 此應用設計為恰好 5 個類別。若要變更類別：

1. **更新 Excel 檔案** (`問答題庫範本.xlsx`):
   - 修改 `類別` 欄位為新類別名稱
   - 每個類別維持 10 題以保持平衡

2. **更新圖示對應** 在 `index.html`:
   ```javascript
   const categoryIcons = {
       '新類別名稱': 'fas fa-icon-name',  // 新增類別
       // ... 其他類別
   };
   ```

3. **重啟 Flask 伺服器** 以重新載入 Excel 資料

4. API 會自動偵測並提供新類別（無需修改程式碼）

### 修改運動影片展示
**位置**: `punishment_videos.html`（完整中文註解）

新增/移除影片：
1. 更新 JavaScript 中的 `mediaFiles` 陣列（約第 368 行）
2. 將影片/圖片檔案加入 `影片/` 目錄
3. 無需重啟伺服器（靜態檔案）

### 自訂 UI 主題
- **顏色**: 修改任何 HTML 檔案中的 CSS `:root` 變數
- **玻璃擬物化**: 調整 `backdrop-filter: blur()` 值
- **動畫**: 編輯 `@keyframes` 定義
- **圖示**: 變更 `categoryIcons` 物件中的 FontAwesome 類別

### 音效系統修改
- **位置**: `question_display.html` > `SoundManager` 類別
- **新增音效**: 擴充 `sounds` 物件，加入新的 {frequency, duration, type}
- **調整音調**: 修改頻率值（Hz）
- **時間控制**: 變更持續時間值（毫秒）

### 程式碼文件標準
- `punishment_videos.html` 作為**文件範例** - 每一行都有詳細中文註解
- 建立新 HTML 頁面時，遵循相同註解風格
- 使用區段分隔符如 `/* =========== 區段名稱 =========== */`
- 說明「為什麼」而非只說「是什麼」（例如：「絕對定位在右上角」而非只寫 "position: absolute"）

### 新增詳解到題目
在 Excel 的 `詳解` 欄位加入說明文字：
- 答錯時會在回饋頁面顯示詳解
- 詳解會透過 URL 參數傳遞：`/feedback_incorrect?explanation=詳解內容`
- 在 `feedback_incorrect.html` 中使用 JavaScript 解析並顯示

## 部署考量

### PyInstaller 打包
- **打包支援**: 可使用 PyInstaller 打包為獨立執行檔
- **路徑解析**: 透過 `getattr(sys, 'frozen', False)` 處理開發與打包環境
- **資源管理**: Tailwind CSS 和 FontAwesome 透過 CDN 載入
- **跨平台**: Windows 批次檔 + Python 跨平台核心
- **檔案包含**: 確保 `影片/` 目錄和 `問答題庫範本.xlsx` 包含在打包中

### 環境變數
- `FLASK_SECRET_KEY`: 設定 Flask session 密鑰（生產環境建議）
- `FLASK_ENV=production`: 關閉 debug 模式（生產環境）

### 替代啟動模式
**控制台模式**（預設）:
```bash
python app.py
```

**Tkinter GUI 模式**（程式碼中已實作但未啟用）:
- 取消註解 `app.py` 末尾的 `create_ui()` 呼叫
- 提供圖形化啟動介面
- 自動開啟瀏覽器
