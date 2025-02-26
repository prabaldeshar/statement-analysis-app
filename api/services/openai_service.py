
from openai import OpenAI

from api.services.system_prompt import response_format, system_prompt
from api.config.settings import settings


class OpenAIService:
    def __init__(self):
        self.openai_api_key = settings.OPENAI_API_KEY
        self.client = OpenAI(api_key=self.openai_api_key)

    def infer(self, user_input: str) -> dict:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": [{"type": "text", "text": system_prompt}],
                },
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
