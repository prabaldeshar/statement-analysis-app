import os

from dotenv import load_dotenv
from openai import OpenAI
from api.services.system_prompt import response_format, system_prompt

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


def infer(user_input: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
            {"role": "user", "content": [{"type": "text", "text": user_input}]},
        ],
        response_format=response_format,
        temperature=1,
        max_completion_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    response_choices = response.choices[0].message.content
    response_dict = eval(response_choices)

    return response_dict
