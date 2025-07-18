import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY")
