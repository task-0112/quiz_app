from openai import OpenAI

class QuizGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def generate_quiz(self, genre):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたはクイズ作成者です。"},
                {"role": "user", "content": f"{genre}に関する問題を1問作成してください。形式は「問題:」の形で出力してください。"}
            ],
            temperature=0
        )
        return response.choices[0].message.content