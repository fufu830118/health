# 🎲 安全健康知識大富翁活動

現代化的中文健康教育問答應用，採用 **Supabase 雲端資料庫 + 純前端 SPA 架構**。

![](https://img.shields.io/badge/Supabase-3ECF8E?style=flat&logo=supabase&logoColor=white)
![](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white)

## ✨ 功能特色

### 核心功能
- ✅ **315 題專業題庫** - 涵蓋健康、環保、安全、衛生、防災五大類別
- ✅ **單頁應用架構** - 流暢頁面切換，無需重新載入
- ✅ **30 秒倒數計時** - 視覺化警告（10秒黃色、5秒紅色）+ 暫停功能
- ✅ **智慧回饋系統** - 顯示使用者選擇與正確答案對比
- ✅ **詳細解答** - 答錯時顯示專業詳解
- ✅ **計時器修正** - 每次答題正確從 30 秒重新開始

### 互動功能
- ✅ **鍵盤快捷鍵** - 數字鍵選題、空白鍵控制
- ✅ **散場音樂** - 點擊標題切換音樂
- ✅ **智慧型運動計時器** - 8 個運動示範，依影片類型自動調整：
  - 彈力帶30下、深蹲15下：60秒計時（影片靜音+背景音樂）
  - 拳擊有氧60秒：60秒計時（保留影片聲音）
  - 瑜珈姿勢：60秒計時+警告提示卡片
- ✅ **音效系統優化** - 答對/答錯後 3 秒自動播放主選單音樂

### UI/UX
- ✅ **玻璃擬物化 UI** - 未來感設計配合動態粒子背景
- ✅ **響應式設計** - 完美支援手機、平板、桌面
- ✅ **字體尺寸優化** - 題目字體比選項大 1.2 倍，易於閱讀

## 🚀 快速開始

### 1. 設定 Supabase

#### 步驟 1：建立專案
1. 前往 [Supabase](https://supabase.com/) 註冊並登入
2. 點擊 "New Project"
3. 填寫專案名稱、資料庫密碼、選擇區域
4. 等待專案建立完成（約 2 分鐘）

#### 步驟 2：建立資料表
在 Supabase Dashboard 左側選單選擇 **SQL Editor**，執行以下 SQL：

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

-- 設定公開讀取權限
ALTER TABLE questions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public SELECT" ON questions FOR SELECT USING (true);

-- 建立索引加速查詢
CREATE INDEX idx_questions_category ON questions(category);
CREATE INDEX idx_questions_appeared ON questions(appeared);
```

#### 步驟 3：匯入題庫
1. 在 Supabase Dashboard 左側選單選擇 **Table Editor**
2. 選擇 `questions` 資料表
3. 點擊右上角 "Insert" > "Import data from CSV"
4. 上傳 `supabase_questions.csv` 檔案
5. 確認欄位對應正確後匯入
6. 驗證：應顯示 315 筆資料

#### 步驟 4：取得連線資訊
1. 在 Supabase Dashboard 選擇 **Settings** > **API**
2. 複製以下資訊：
   - **Project URL**: `https://your-project.supabase.co`
   - **anon public key**: `eyJhbGciOi...` （很長的字串）

### 2. 設定專案

#### 更新 Supabase 連線
編輯 `supabase-client.js` 檔案：

```javascript
const SUPABASE_URL = "https://your-project.supabase.co";  // 替換成您的 Project URL
const SUPABASE_KEY = "your-anon-key";  // 替換成您的 anon public key
```

### 3. 執行應用

使用以下任一方法啟動本機伺服器：

```bash
# 方法 1: Python 內建伺服器（推薦）
python -m http.server 8000

# 方法 2: VS Code Live Server
# 安裝 Live Server 擴充 → 右鍵 index.html → Open with Live Server

# 方法 3: Node.js http-server
npx http-server -p 8000
```

開啟瀏覽器，前往 `http://localhost:8000`

## 📁 檔案結構

```
health-quiz/
├── index.html                  # 單頁應用主檔案（包含所有頁面）
│   ├── page-menu              # 主選單
│   ├── page-question          # 答題頁面
│   ├── page-correct           # 答對回饋
│   ├── page-incorrect         # 答錯回饋（含正確答案對比）
│   ├── page-timeout           # 超時回饋
│   └── page-videos            # 運動影片展示
├── supabase-client.js         # Supabase 連線層
├── supabase_questions.csv     # 題庫 CSV (315題)
├── supabase_questions.xlsx    # 題庫 Excel 備份
├── 影片/                       # 運動影片資料夾
│   ├── 全組開合跳30秒.mp4
│   ├── 全組深蹲30秒.mp4
│   ├── 深蹲15下.mp4
│   ├── 弓箭步30秒.mp4
│   └── ...（共8個檔案）
└── 音效/                       # 音效資料夾
    ├── 背景音樂.mp3           # 主選單音樂
    ├── 答題音樂.mp3           # 答題音樂
    ├── 散場音樂.mp3           # 結束音樂
    ├── 倒數背景音樂.m4a       # 運動計時器音樂
    ├── 答對.wav
    └── 答錯.wav
```

## 🎯 題庫類別

| 類別 | 題數 | 主題範圍 |
|------|------|---------|
| 健康題 | 63 題 | 食品安全、營養標示、用藥安全、菸害防制 |
| 環保題 | 63 題 | 環保法規、污染防治、水質保護、廢棄物處理 |
| 安全題 | 63 題 | 職業安全、工安法規、防護措施、作業安全 |
| 衛生題 | 63 題 | 個人衛生、傳染病防治、環境清潔 |
| 防災題 | 63 題 | 防災準備、應變措施、緊急逃生 |
| **總計** | **315 題** | 完整專業題庫 |

## 🎨 技術棧

### 前端技術
- **Vanilla JavaScript** - 純 JavaScript，無框架依賴
- **Tailwind CSS** (CDN) - 實用優先 CSS 框架
- **FontAwesome 6** (CDN) - 圖示庫
- **Web Audio API** - 即時音效生成

### 後端服務
- **Supabase** - PostgreSQL 資料庫
- **Supabase Auth** - Row Level Security (RLS)
- **Supabase Realtime** - 即時資料更新（可選）

### UI 設計
- 玻璃擬物化設計（Glassmorphism）
- 動態粒子背景動畫
- CSS Grid 響應式佈局
- Mobile-first 設計

## 🛠️ 開發指南

### 新增題目
1. 編輯 `supabase_questions.csv`（UTF-8 with BOM 編碼）
2. 登入 Supabase Dashboard
3. Table Editor > questions > 刪除舊資料
4. 重新匯入 CSV
5. 重新整理瀏覽器

### 修改類別圖示
編輯 `index.html` 中的 `categoryIcons` 物件：

```javascript
const categoryIcons = {
    '健康題': 'fas fa-heartbeat',
    '環保題': 'fas fa-recycle',
    '安全題': 'fas fa-shield-alt',
    '衛生題': 'fas fa-hands-wash',
    '防災題': 'fas fa-exclamation-triangle'
};
```

### 更新運動影片
編輯 `index.html` 中的 `mediaFiles` 陣列（page-videos 區域）：

```javascript
const mediaFiles = [
    { name: '全組開合跳30秒', file: '全組開合跳30秒.mp4', type: 'video', duration: 30 },
    { name: '彈力帶30下', file: '彈力帶30下.mp4', type: 'video', duration: 60 },
    { name: '拳擊有氧60秒', file: '拳擊有氧60秒.mp4', type: 'video', duration: 60, keepVideoSound: true },
    { name: '瑜珈姿勢示範', file: '拍瑜珈型態照片1張.jpg', type: 'image', duration: 60 },
    // ... 新增更多影片
    // duration: 計時器秒數（0 表示無計時器）
    // keepVideoSound: true 表示保留影片聲音，不播放背景音樂
];
```

### 自訂主題顏色
修改任何 HTML 檔案中的 CSS 變數：

```css
:root {
    --accent-cyan: #06b6d4;
    --accent-purple: #a855f7;
    --accent-pink: #ec4899;
    --accent-red: #ef4444;
}
```

## 📦 部署指南

### GitHub Pages（推薦）
```bash
# 1. 推送程式碼到 GitHub
git add .
git commit -m "Deploy quiz app"
git push origin main

# 2. 在 GitHub repo > Settings > Pages
#    Source: Deploy from a branch
#    Branch: main / (root)
#    Save

# 3. 存取網址：https://your-username.github.io/repo-name/
```

### Vercel
```bash
# 安裝 Vercel CLI
npm i -g vercel

# 部署
vercel

# 生產環境
vercel --prod
```

### Netlify
1. 拖曳專案資料夾到 [Netlify Drop](https://app.netlify.com/drop)
2. 或連接 GitHub repo 自動部署

## 🔧 疑難排解

### 題目無法載入？
✅ 檢查 `supabase-client.js` 中的 URL 和 Key 是否正確
✅ 開啟瀏覽器 Console (F12) 查看錯誤訊息
✅ 確認 Supabase RLS Policy 已設定為公開讀取
✅ 驗證資料表中有 315 筆資料

### 中文字顯示亂碼？
✅ 確認 CSV 使用 UTF-8 with BOM 編碼
✅ 檢查 HTML 有 `<meta charset="UTF-8">`
✅ Supabase 匯入時選擇 UTF-8 編碼

### 影片無法播放？
✅ 檢查影片格式（建議 MP4）
✅ 確認檔案路徑正確（相對路徑）
✅ 查看瀏覽器 Console 是否有載入錯誤

### 音效無聲？
✅ Web Audio API 需要用戶互動才能啟動
✅ 檢查瀏覽器是否阻擋自動播放
✅ 某些瀏覽器（Safari）可能需要額外權限

## 📄 授權

MIT License

## 👨‍💻 作者

健康知識問答系統

## 🙏 致謝

- [Supabase](https://supabase.com/) - 開源 Firebase 替代方案
- [Tailwind CSS](https://tailwindcss.com/) - CSS 框架
- [FontAwesome](https://fontawesome.com/) - 圖示庫

---

**需要幫助？** 請開啟 [Issue](https://github.com/your-username/health-quiz/issues) 或查看 [CLAUDE.md](CLAUDE.md) 詳細開發文件。
