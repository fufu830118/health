// Supabase 連線設定
const SUPABASE_URL = "https://imyhrdhbiqoosxepiglu.supabase.co";
const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlteWhyZGhiaXFvb3N4ZXBpZ2x1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE5NjUwMTAsImV4cCI6MjA3NzU0MTAxMH0.wu19Weeb8UzdXUDJtBszzCeLzpLRI8uKu303xhfZAFQ";

const supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

// 取得所有問題類別
async function getCategories() {
    const { data, error } = await supabaseClient
        .from('questions')
        .select('category');

    if (error) {
        console.error('取得類別失敗:', error);
        return [];
    }

    return [...new Set(data.map(item => item.category))];
}

// 取得指定類別的隨機題目 (只抓取未出現過的題目)
async function getRandomQuestion(category) {
    const { data, error } = await supabaseClient
        .from('questions')
        .select('*')
        .eq('category', category)
        .eq('appeared', false);  // 只抓取 appeared = false 的題目

    if (error || !data || data.length === 0) {
        console.error('取得題目失敗或該類別沒有未使用的題目:', error);
        return null;
    }

    const randomIndex = Math.floor(Math.random() * data.length);
    return data[randomIndex];
}

// 驗證答案
async function checkAnswer(questionId, userAnswer) {
    const { data, error } = await supabaseClient
        .from('questions')
        .select('*')
        .eq('id', questionId)
        .single();

    if (error || !data) {
        console.error('驗證答案失敗:', error);
        return { error: true };
    }

    const isCorrect = data.correct.toUpperCase() === userAnswer.toUpperCase();

    return {
        isCorrect: isCorrect,
        correctAnswer: data.correct,
        explanation: data.explanation || ''
    };
}

// 標記題目為已出現
async function markQuestionAsAppeared(questionId) {
    const { data, error } = await supabaseClient
        .from('questions')
        .update({ appeared: true })
        .eq('id', questionId);

    if (error) {
        console.error('更新appeared失敗:', error);
        return false;
    }

    console.log('題目已標記為appeared:', questionId);
    return true;
}
