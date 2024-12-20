import streamlit as st
import os
from dotenv import load_dotenv
from quiz_generator import QuizGenerator
from grader import Grader
from feedback_generator import FeedbackGenerator

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
    st.title("クイズアプリ")
    
    # セッション状態の初期化
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = None
    if 'result' not in st.session_state:
        st.session_state.result = None
    if 'feedback' not in st.session_state:
        st.session_state.feedback = None
    
    # ジャンル入力
    genre = st.text_input("クイズのジャンルを入力してください")
    
    if st.button("クイズを生成"):
        quiz = quiz_gen.generate_quiz(genre)
        st.session_state.quiz_data = quiz
        # 新しいクイズを生成したら結果とフィードバックをリセット
        st.session_state.result = None
        st.session_state.feedback = None
    
    # クイズデータの表示
    if st.session_state.quiz_data:
        st.write("問題:", st.session_state.quiz_data)
        
        user_answer = st.text_input("回答を入力してください")
        
        if st.button("回答する"):
            st.session_state.result = grader.grade_answer(st.session_state.quiz_data, "正解", user_answer)
            st.session_state.feedback = feedback_gen.generate_feedback(
                st.session_state.quiz_data, 
                "正解", 
                user_answer, 
                st.session_state.result
            )
    
    # 結果とフィードバックの表示
    if st.session_state.result and st.session_state.feedback:
        st.title("判定結果")
        st.write(st.session_state.result)
        st.title("フィードバック")
        st.write(st.session_state.feedback)
    # クリアボタン
    if st.button("クリア"):
        st.session_state.quiz_data = None
        st.session_state.result = None
        st.session_state.feedback = None
        st.experimental_rerun()

if __name__ == "__main__":
    main()