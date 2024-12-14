from openai import OpenAI
import os


class GPTClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def Ans_GPT(self, instruction, question):
        response = self.client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system","content": instruction},
            {"role": "user","content": question}
        ],
        temperature=0
        )
        res = response.choices[0].message.content
        return res