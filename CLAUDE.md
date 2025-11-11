# CLAUDE.md

本檔案為 Claude Code (claude.ai/code) 提供此專案的開發指引。

## 專案概述

這是一個現代化的中文健康教育問答應用，採用 **Supabase 雲端資料庫 + 純前端 SPA 架構**。主要特色包括：未來感玻璃擬物化 UI、Web Audio API 音效系統、專業題庫 315 題，以及運動懲罰影片展示系統。

### 最新功能更新（2025）
- ✅ **單頁應用架構** - 所有功能整合在 index.html，無需多頁面切換
- ✅ **運動影片增強** - 影片循環播放、計時器播放時靜音、倒數背景音樂
- ✅ **暫停功能優化** - 切換頁面時自動重置暫停狀態
- ✅ **答題回饋改進** - 顯示使用者選擇和正確答案對比
- ✅ **鍵盤快捷鍵** - 空白鍵控制暫停/返回主選單
- ✅ **散場音樂功能** - 點擊標題切換散場音樂和背景音樂
- ✅ **UI 尺寸優化** - 放大字體和按鈕，適應 100% 縮放無滾動條

## 架構說明

### 資料庫架構（Supabase）
- **雲端資料庫**: 使用 Supabase PostgreSQL 儲存題目資料
- **題庫管理系統**:
  - 從 `supabase_questions.csv` 匯入 315 題專業題庫
  - 資料表欄位：id, category, question, option_a, option_b, option_c, correct, explanation, appeared
  - 共 315 題，分布於 5 個類別（健康題、環保題、安全題、衛生題、防災題）
  - `appeared` 欄位追蹤已使用題目，避免重複出題（前端管理）
  - 具備 Row Level Security (RLS) 安全性設定
- **題庫備份檔案**:
  - `supabase_questions.csv` - UTF-8 編碼的 CSV 格式（315 題，用於匯入 Supabase）
  - `supabase_questions.xlsx` - Excel 備份檔案

### 前端架構（純 SPA）
- **無需後端伺服器**: 純前端應用，直接連接 Supabase
- **Supabase Client** (`supabase-client.js`):
  - 資料庫連線層，封裝 Supabase JavaScript 客戶端
  - 提供題目查詢 API：`getRandomQuestion(category)`, `markQuestionAsUsed(id)` 等
  - 處理已使用題目的前端快取
- **靜態檔案**:
  - 影片/圖片檔案位於 `影片/` 目錄
  - 音效檔案位於 `音效/` 目錄
  - 可使用任何靜態伺服器（如 Python http.server, VS Code Live Server, GitHub Pages）

### 問題類別（固定 5 個）
應用支援精確 5 個問題類別，共 315 題：
1. **健康題** - `fas fa-heartbeat` 圖示（醫療、飲食、用藥等）
2. **環保題** - `fas fa-recycle` 圖示（環保法規、污染防治等）
3. **安全題** - `fas fa-shield-alt` 圖示（職業安全、工安法規等）
4. **衛生題** - `fas fa-hands-wash` 圖示（個人衛生、疾病防治等）
5. **防災題** - `fas fa-exclamation-triangle` 圖示（防災準備、應變措施等）

### 前端頁面架構（單頁應用）
- **主選單頁面** (`index.html` - page-menu):
  - 🎲 標題「安全健康知識大富翁活動」可點擊切換散場音樂
  - 玻璃擬物化設計配合動態粒子背景
  - 5 個類別按鈕（1行5列固定佈局）+ 運動懲罰示範按鈕
  - 從 Supabase API 動態載入類別，搭配自訂 FontAwesome 圖示
  - 鍵盤快捷鍵：數字鍵 1-5 選擇類別

- **答題頁面** (`index.html` - page-question):
  - 30 秒倒數計時器，視覺警告（10 秒黃色、5 秒紅色）
  - 暫停/繼續功能（空白鍵控制）
  - 三選一選項（數字鍵 1-3 選擇，連按兩次送出）
  - 玻璃擬物化按鈕互動與動畫
  - 切換頁面時自動重置暫停狀態

- **答對頁面** (`index.html` - page-correct):
  - ✅ 圖示 + 「恭喜答對！你可以留在原地！」同一行
  - 顯示使用者選擇的選項（綠色漸層框）
  - 顯示詳解（可選）
  - 空白鍵返回主選單

- **答錯頁面** (`index.html` - page-incorrect):
  - ❌ 圖示 + 「很遺憾答錯了！請回到上一個擲骰子的位置！」同一行
  - 顯示使用者選擇的錯誤選項（第一行）
  - 顯示正確答案（第二行，綠色文字）
  - 紅色漸層框強調錯誤
  - 顯示詳解（可選）
  - 空白鍵返回主選單

- **超時頁面** (`index.html` - page-timeout):
  - ⏰ 圖示 + 超時訊息
  - 空白鍵返回主選單

- **運動懲罰影片展示** (`index.html` - page-videos):
  - 網格佈局顯示 8 個運動影片（從 `影片/` 資料夾）
  - 模態視窗 16:9 全螢幕影片播放
  - 影片循環播放
  - 計時器功能：
    - 按播放鍵：影片靜音、播放倒數背景音樂、停用 AI 語音
    - 按重置鍵：影片聲音恢復
  - 空白鍵返回主選單

### 現代化 UI 特色
- **玻璃擬物化設計**: 背景模糊效果配合半透明容器
- **動態粒子背景**: 純 CSS 動畫浮動粒子效果
- **Web Audio API 音效系統**:
  - 即時音調生成（無需外部音效檔案）
  - 情境音效（tick、warning、success、error）
  - 用戶互動觸發音效上下文初始化
- **進階響應式設計**: Mobile-first 設計搭配 Tailwind CSS
- **流暢動畫**: CSS 過渡、變形和關鍵影格動畫

## Supabase 設定

### 1. 建立 Supabase 專案
1. 前往 [Supabase](https://supabase.com/) 建立帳號
2. 建立新專案（選擇區域、設定密碼）
3. 等待專案建立完成

### 2. 建立資料表
在 Supabase Dashboard > SQL Editor 執行以下 SQL：

```sql
CREATE TABLE questions (
    id BIGSERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    question TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    correct TEXT NOT NULL CHECK (correct IN ('A', 'B', 'C')),
    explanation TEXT,
    appeared BOOLEAN DEFAULT false
);

-- 設定 RLS Policy（允許公開讀取）
ALTER TABLE questions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public SELECT" ON questions FOR SELECT USING (true);

-- 建立索引以加速查詢
CREATE INDEX idx_questions_category ON questions(category);
CREATE INDEX idx_questions_appeared ON questions(appeared);
```

### 3. 匯入題庫資料
使用 Supabase Dashboard > Table Editor:
1. 選擇 `questions` 資料表
2. 點擊 "Insert" > "Import data from CSV"
3. 上傳 `supabase_questions.csv` 檔案
4. 確認欄位對應正確
5. 匯入完成，應該有 315 筆資料

### 4. 更新連線設定
編輯 `supabase-client.js`，填入您的 Supabase 專案資訊：

```javascript
const SUPABASE_URL = "https://your-project.supabase.co";  // 替換成您的 Project URL
const SUPABASE_KEY = "your-anon-key";  // 替換成您的 anon public key
```

取得方式：
- Project URL: Supabase Dashboard > Settings > API > Project URL
- anon key: Supabase Dashboard > Settings > API > Project API keys > anon public

## 常用開發指令

### 執行應用程式（本機開發）
```bash
# 方法 1: 使用 Python 內建伺服器
python -m http.server 8000
# 瀏覽器開啟: http://localhost:8000

# 方法 2: 使用 VS Code Live Server 擴充功能
# 右鍵 index.html > Open with Live Server

# 方法 3: 使用 Node.js http-server
npx http-server -p 8000
```

### 更新題庫資料
修改 `supabase_questions.csv` 後：
1. 登入 Supabase Dashboard
2. Table Editor > questions
3. 刪除舊資料或使用 SQL：`TRUNCATE TABLE questions RESTART IDENTITY;`
4. 重新匯入 CSV 檔案
5. 重新整理瀏覽器即可看到更新

### 題庫編碼注意事項
- CSV 檔案必須使用 **UTF-8 with BOM** 編碼
- 確保中文字元不會亂碼
- Python 讀寫時使用 `encoding='utf-8-sig'`

```python
import csv

# 讀取 CSV
with open('supabase_questions.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# 寫入 CSV
with open('supabase_questions.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['category', 'question', ...])
    writer.writeheader()
    writer.writerows(rows)
```

## 檔案結構

### 核心應用檔案
- `index.html` - 單頁應用主檔案（包含所有頁面）
  - page-menu: 主選單
  - page-question: 答題頁面
  - page-correct: 答對回饋
  - page-incorrect: 答錯回饋
  - page-timeout: 超時回饋
  - page-videos: 運動影片展示
- `supabase-client.js` - Supabase 連線層與 API 封裝
- `影片/` - 運動影片目錄（8 個 MP4/JPG 檔案）
- `音效/` - 音效檔案目錄
  - `背景音樂.mp3` - 主選單背景音樂
  - `答題音樂.mp3` - 答題頁面音樂
  - `散場音樂.mp3` - 結束音樂
  - `倒數背景音樂.m4a` - 運動計時器音樂
  - `答對.wav` / `答錯.wav` - 答題音效

### 題庫資料檔案
- `supabase_questions.csv` - UTF-8 編碼的 CSV 格式（315 題）
- `supabase_questions.xlsx` - Excel 備份檔案

### HTML 檔案技術棧
所有 HTML 檔案使用：
- **Tailwind CSS** via CDN - 實用優先樣式框架
- **FontAwesome 6** - 現代化圖示庫
- **Supabase JavaScript Client** via CDN
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

1. **啟動**: 使用靜態伺服器開啟 `index.html`
2. **主選單**: 5 個類別按鈕 + 1 個運動影片展示按鈕
3. **類別選擇**: 點擊類別從 Supabase 載入隨機題目
4. **問題顯示**: 30 秒動畫倒數計時，配合音效
5. **提交答案**: 前端驗證答案並導向回饋頁面
6. **顯示詳解**: 答錯時顯示來自資料庫的詳解
7. **進度追蹤**: 前端快取已使用題目 ID，避免重複
8. **類別完成**: 所有題目答完後顯示完成通知

## 技術實作細節

### Supabase 整合
- **Supabase JavaScript Client**: 透過 CDN 載入官方客戶端
- **查詢隨機題目**: 使用 `ORDER BY RANDOM() LIMIT 1` SQL 查詢
- **已使用題目快取**: 前端 LocalStorage 儲存已答過的題目 ID
- **錯誤處理**: API 失敗時顯示友善錯誤訊息
- **安全性**: 使用 RLS Policy 保護資料，僅允許公開讀取

```javascript
// 範例：查詢隨機題目
async function getRandomQuestion(category) {
    const usedIds = JSON.parse(localStorage.getItem(`used_${category}`) || '[]');

    let query = supabase
        .from('questions')
        .select('*')
        .eq('category', category);

    if (usedIds.length > 0) {
        query = query.not('id', 'in', `(${usedIds.join(',')})`);
    }

    const { data, error } = await query.order('id', { ascending: false }).limit(100);
    if (error) throw error;

    // 隨機選擇一題
    const randomIndex = Math.floor(Math.random() * data.length);
    return data[randomIndex];
}
```

### 音效系統架構
- **Web Audio API**: 純 JavaScript 音調生成
- **音效類型**: click、hover、tick、warning、critical、timeout、success、error
- **上下文管理**: 用戶觸發音效上下文，符合瀏覽器相容性
- **漸進增強**: 音效無法使用時優雅降級

### 影片展示系統
- **響應式網格**: CSS Grid 使用 `repeat(auto-fill, minmax(320px, 1fr))`
- **模態系統**: 全螢幕覆蓋層影片播放
- **媒體偵測**: 自動處理影片和圖片檔案類型
- **事件處理**: 點擊、ESC 鍵、背景點擊關閉模態視窗

### 響應式設計策略
- **Mobile-First**: 基礎樣式針對行動裝置優化
- **漸進增強**: 透過媒體查詢新增桌面功能
- **觸控友善**: 行動裝置上的大型按鈕和觸控目標
- **效能優化**: 優化動畫和過渡效果

## 開發注意事項

### 新增問題類別
若要新增或修改類別：

1. **更新 CSV 檔案** (`supabase_questions.csv`):
   - 新增題目並設定 `category` 欄位為新類別名稱
   - 匯入到 Supabase

2. **更新圖示對應** 在 `index.html`:
   ```javascript
   const categoryIcons = {
       '新類別名稱': 'fas fa-icon-name',  // 新增類別
       // ... 其他類別
   };
   ```

3. **重新整理瀏覽器** 即可看到新類別

### 修改運動影片展示
**位置**: `punishment_videos.html`

新增/移除影片：
1. 更新 JavaScript 中的 `mediaFiles` 陣列
2. 將影片/圖片檔案加入 `影片/` 目錄
3. 重新整理瀏覽器即可

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

### 新增詳解到題目
在 CSV 的 `explanation` 欄位加入說明文字：
- 答錯時會在回饋頁面顯示詳解
- 詳解會透過 URL 參數傳遞：`/feedback_incorrect.html?explanation=詳解內容`
- 在 `feedback_incorrect.html` 中使用 JavaScript 解析並顯示

## 部署選項

### 1. GitHub Pages（推薦）
```bash
# 推送到 GitHub
git add .
git commit -m "Update quiz app"
git push origin main

# 在 GitHub repo > Settings > Pages
# Source: Deploy from a branch
# Branch: main / (root)
```

存取網址：`https://your-username.github.io/your-repo-name/`

### 2. Vercel
```bash
# 安裝 Vercel CLI
npm i -g vercel

# 部署
vercel

# 生產環境部署
vercel --prod
```

### 3. Netlify
1. 將專案推送到 GitHub
2. 登入 [Netlify](https://netlify.com)
3. New site from Git > 選擇 repo
4. Build settings: 留空（純靜態網站）
5. Deploy site

### 部署注意事項
- ✅ 確保 `supabase-client.js` 中的 Supabase URL 和 Key 已填入
- ✅ 檢查所有檔案路徑使用相對路徑（非絕對路徑）
- ✅ 影片檔案大小檢查（GitHub 單檔 100MB 限制）
- ✅ CORS 設定：Supabase 預設允許所有來源（生產環境可限制）

## 疑難排解

### 題目無法載入
1. 檢查 Supabase URL 和 Key 是否正確
2. 開啟瀏覽器 Console 查看錯誤訊息
3. 確認 Supabase RLS Policy 已設定為公開讀取
4. 檢查 `questions` 資料表是否有資料

### 中文字元亂碼
1. 確認 CSV 檔案使用 UTF-8 with BOM 編碼
2. 檢查 HTML 檔案有 `<meta charset="UTF-8">`
3. Supabase 匯入時選擇正確編碼

### 影片無法播放
1. 檢查影片檔案格式（建議 MP4）
2. 確認檔案路徑正確（相對路徑）
3. 瀏覽器 Console 查看載入錯誤
4. 檢查檔案大小（過大可能載入慢）

### 音效無法播放
1. Web Audio API 需要用戶互動才能啟動
2. 檢查瀏覽器是否阻擋自動播放
3. 查看 Console 是否有 AudioContext 錯誤
4. 某些瀏覽器（如 Safari）可能需要額外設定
