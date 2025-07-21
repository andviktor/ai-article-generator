from openai import OpenAI
from openai.types.images_response import ImagesResponse

from app.config import Config


class OpenAIClient:
    def __init__(self) -> None:
        self.client: OpenAI = OpenAI(api_key=Config.OPENAI_API_KEY)

    def request(
        self, prompt: str, task: str, width: int, height: int, quality: str
    ) -> str:
        response: ImagesResponse = self.client.images.generate(
            model="dall-e-3",
            prompt=f"{prompt} Text to illustrate: {task}",
            size=f"{width}x{height}",  # type: ignore
            quality=quality,  # type: ignore
            n=1,
        )
        return response.data[0].url  # type: ignore
