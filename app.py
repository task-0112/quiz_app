import streamlit as st
import os
from dotenv import load_dotenv
from quiz_generator import QuizGenerator
from grader import Grader
from feedback_generator import FeedbackGenerator

# ページ設定
st.set_page_config(
    page_title="AI Quiz App",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="expanded",
)

# カスタムCSS
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .main-header {
        text-align: center;
        padding: 20px;
    }
    .feedback-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .correct {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
    }
    .incorrect {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# .envファイルの読み込み
load_dotenv()

# 環境変数の取得
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    st.error("OpenAI API キーが設定されていません。.envファイルを確認してください。")
    st.stop()

# インスタンス作成
quiz_gen = QuizGenerator(api_key)
grader = Grader(api_key)
feedback_gen = FeedbackGenerator(api_key)

def main():
    st.markdown("<h1 class='main-header'>🎯 AIクイズマスター</h1>", unsafe_allow_html=True)
    
    # セッション状態の初期化
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = None
    if 'result' not in st.session_state:
        st.session_state.result = None
    if 'feedback' not in st.session_state:
        st.session_state.feedback = None
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = 0

    # サイドバー
    with st.sidebar:
        st.header("クイズ設定")
        genre = st.selectbox(
            "ジャンルを選択してください",
            ["一般常識", "科学", "歴史", "文学", "スポーツ", "音楽", "映画", "その他"]
        )
        
        if genre == "その他":
            genre = st.text_input("ジャンルを入力してください")
        
        difficulty = st.select_slider(
            "難易度を選択",
            options=["初級", "中級", "上級"],
            value="中級"
        )

        st.markdown("---")
        st.markdown("### 📊 成績")
        if st.session_state.total_questions > 0:
            accuracy = (st.session_state.correct_answers / st.session_state.total_questions) * 100
            st.progress(accuracy / 100)
            st.markdown(f"正答率: {accuracy:.1f}%")
            st.markdown(f"回答数: {st.session_state.total_questions}")

    # メインコンテンツ
    if 'quiz_data' not in st.session_state:
        st.info("👈 サイドバーでジャンルを選択し、クイズを始めましょう！")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("🎲 新しいクイズを生成", key="generate"):
            with st.spinner("クイズを生成中..."):
                quiz = quiz_gen.generate_quiz(f"{difficulty}レベルの{genre}")
                st.session_state.quiz_data = quiz
                st.session_state.result = None
                st.session_state.feedback = None
    
    with col2:
        if st.button("🔄 リセット", key="reset"):
            st.session_state.quiz_data = None
            st.session_state.result = None
            st.session_state.feedback = None
            st.session_state.total_questions = 0
            st.session_state.correct_answers = 0
            st.experimental_rerun()

    # クイズの表示
    if st.session_state.quiz_data:
        st.markdown("---")
        st.markdown("### 📝 問題")
        st.markdown(f"_{st.session_state.quiz_data}_")
        
        with st.form(key='quiz_form'):
            user_answer = st.text_input("あなたの回答を入力してください", key="answer")
            submit = st.form_submit_button("回答を送信")
            
            if submit and user_answer:
                with st.spinner("採点中..."):
                    result = grader.grade_answer(st.session_state.quiz_data, "正解", user_answer)
                    feedback = feedback_gen.generate_feedback(
                        st.session_state.quiz_data, 
                        "正解", 
                        user_answer, 
                        result
                    )
                    st.session_state.result = result
                    st.session_state.feedback = feedback
                    st.session_state.total_questions += 1
                    if "正解" in result:
                        st.session_state.correct_answers += 1

    # 結果とフィードバックの表示
    if st.session_state.result and st.session_state.feedback:
        st.markdown("---")
        is_correct = "正解" in st.session_state.result
        result_class = "correct" if is_correct else "incorrect"
        
        st.markdown(f"""
            <div class='feedback-box {result_class}'>
                <h3>{'🎉 正解！' if is_correct else '😢 不正解'}</h3>
                <p>{st.session_state.result}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💡 フィードバック")
        st.info(st.session_state.feedback)

if __name__ == "__main__":
    main()