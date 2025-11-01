# 健康知識問答系統 - Supabase 版

純前端健康教育問答應用，使用 Supabase 雲端資料庫。

## 🚀 快速開始

### 1. 設定 Supabase

1. 登入 [Supabase](https://supabase.com/)
2. 建立新專案
3. 建立 `questions` 資料表：

```sql
CREATE TABLE questions (
    id BIGSERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    question TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    correct TEXT NOT NULL CHECK (correct IN ('A', 'B', 'C')),
    explanation TEXT
);

-- 設定 RLS Policy
ALTER TABLE questions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public SELECT" ON questions FOR SELECT USING (true);
```

4. 新增題目資料
5. 複製 Project URL 和 anon key

### 2. 更新連線設定

編輯 `supabase-client.js`:

```javascript
const SUPABASE_URL = "您的 Supabase URL";
const SUPABASE_KEY = "您的 anon key";
```

### 3. 執行

使用本機伺服器開啟：

```bash
python -m http.server 8000
# 或
npx http-server -p 8000
```

瀏覽器開啟 `http://localhost:8000`

## 📁 檔案結構

- `index.html` - 主選單
- `question_display.html` - 答題頁面
- `feedback_correct.html` - 答對回饋
- `feedback_incorrect.html` - 答錯回饋
- `timeout_feedback.html` - 逾時回饋
- `punishment_videos.html` - 運動懲罰影片展示
- `supabase-client.js` - Supabase 連線層

## ✨ 功能

- ✅ 30 秒倒數計時
- ✅ 答對/答錯即時回饋
- ✅ 詳解顯示
- ✅ 語音朗讀
- ✅ 音效系統
- ✅ 運動懲罰影片展示
- ✅ 響應式設計

## 🎵 音效檔案

請將音效檔案放在 `音效/` 目錄：
- `答題背景音樂.mp3`
- `答對音效.mp3`
- `答錯音效.mp3`
- `逾時音效.mp3`

## 📝 Supabase 資料表範例

```sql
INSERT INTO questions (category, question, option_a, option_b, option_c, correct, explanation)
VALUES
('健康題', '每天應該喝多少水？', '1公升', '2公升', '3公升', 'B', '成人每天建議攝取約 2 公升的水分'),
('環保題', '哪種垃圾屬於可回收資源？', '廚餘', '寶特瓶', '衛生紙', 'B', '寶特瓶屬於可回收塑膠類');
```

---

**注意**: 此為純前端版本，題目資料從 Supabase 讀取，無需 Flask 伺服器。
