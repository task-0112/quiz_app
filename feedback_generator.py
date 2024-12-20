from openai import OpenAI

class FeedbackGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def generate_feedback(self, question, correct_answer, user_answer, is_correct):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたは教育者です。"},
                {"role": "user", "content": f"問題: {question}\n正解: {correct_answer}\n回答: {user_answer}\n判定: {is_correct}\n詳細なフィードバックを生成してください。"}
            ]
        )
        return response.choices[0].message.content