import openai
import os

openai.api_key = os.environ['OPENAI_API_KEY']
model_name = "gpt-3.5-turbo-0613"

question = "pyenvとpipenvの環境構築方法について教えてください。"

response = openai.ChatCompletion.create(
    model=model_name,
    messages=[
        {"role": "user", "content": question},
    ],
)
print(response.choices[0]["message"]["content"].strip())
