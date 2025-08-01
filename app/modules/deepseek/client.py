from logging import Logger

from openai import OpenAI
from openai.types.chat import ChatCompletion

from app.config import Config


logger = Logger(__name__)


class DeepseekClient:
    def __init__(self) -> None:
        try:
            self.client: OpenAI = OpenAI(
                api_key=Config.DEEPSEEK_API_KEY,
                base_url=Config.DEEPSEEK_BASE_URL,
            )
        except Exception as e:
            logger.error(f"Failed to initialize Deepseek client: {e}")
            raise e

    def request(self, prompt: str, task: str) -> str:
        try:
            response: ChatCompletion = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": task},
                ],
                stream=False,
            )
        except Exception as e:
            logger.error(f"Deepseek request failed: {e}")
            raise e

        return response.choices[0].message.content  # type: ignore
