from openai import OpenAI
from openai.types.chat import ChatCompletion

from app.config import Config


class DeepseekClient:
    def __init__(self) -> None:
        self.client: OpenAI = OpenAI(
            api_key=Config.DEEPSEEK_API_KEY,
            base_url=Config.DEEPSEEK_BASE_URL,
        )

    def request(self, prompt: str, task: str) -> str:
        response: ChatCompletion = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": task},
            ],
            stream=False,
        )

        return response.choices[0].message.content  # type: ignore
