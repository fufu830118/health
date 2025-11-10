-- 步驟1: 清空舊資料
TRUNCATE TABLE questions RESTART IDENTITY;

-- 步驟2: 插入新資料
-- （顯示前3筆作為範例）

INSERT INTO questions (category, question, option_a, option_b, option_c, correct, explanation, appeared)
VALUES ('健康題', '依據食品安全衛生管理法規定，哪一項食品標示不屬於強制標示範圍內?', '品名', '原產地(國)', '業者Line ID', 'C', '食品強制標示項目包括：品名、內容物、食品添加物、有效日期、原產地、營養標示、廠商資訊等。業者Line ID屬私人聯絡方式，非法規強制標示項目。', false);

INSERT INTO questions (category, question, option_a, option_b, option_c, correct, explanation, appeared)
VALUES ('健康題', '下列哪一項食品最可能不含防腐劑？', '醬油', '罐頭', '豆干', 'B', '罐頭透過高溫高壓滅菌及真空密封保存，不需添加防腐劑。醬油、豆干等食品常添加防腐劑（如己二烯酸、苯甲酸）延長保存期限。', false);

INSERT INTO questions (category, question, option_a, option_b, option_c, correct, explanation, appeared)
VALUES ('健康題', '接觸過生雞蛋後要洗手，是為了避免下列何種細菌引起的食物中毒？', '肉毒桿菌', '仙人掌桿菌', '沙門氏菌', 'C', '生雞蛋殼表面常附著沙門氏菌，接觸後未洗手可能造成食物中毒，症狀為腹瀉、發燒、腹痛。肉毒桿菌存於罐頭，仙人掌桿菌存於米飯。', false);

-- ... 共 315 筆資料

-- 完整SQL腳本請使用完整版本
