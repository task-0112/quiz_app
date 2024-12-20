from openai import OpenAI

class Grader:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def grade_answer(self, question, correct_answer, user_answer):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたは採点者です。"},
                {"role": "user", "content": f"問題: {question}\n正解: {correct_answer}\n回答: {user_answer}\n正解か不正解かのみ判定してください。"}
            ],
            temperature=0
        )
        return response.choices[0].message.content