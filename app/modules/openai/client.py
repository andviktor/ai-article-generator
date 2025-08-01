from logging import Logger
from openai import OpenAI
from openai.types.images_response import ImagesResponse

from app.config import Config


logger = Logger(__name__)


class OpenAIClient:
    def __init__(self) -> None:
        try:
            self.client: OpenAI = OpenAI(api_key=Config.OPENAI_API_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise e

    def request(
        self, prompt: str, task: str, width: int, height: int, quality: str
    ) -> str:
        try:
            response: ImagesResponse = self.client.images.generate(
                model="dall-e-3",
                prompt=f"{prompt} Text to illustrate: {task}",
                size=f"{width}x{height}",  # type: ignore
                quality=quality,  # type: ignore
                n=1,
            )
        except Exception as e:
            logger.error(f"OpenAI request failed: {e}")
            raise e

        return response.data[0].url  # type: ignore
