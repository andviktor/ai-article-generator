import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "")
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "")
    AWS_LOCAL_TMP_DIR: str = "aws_tmp"

    PROMPT_CREATE_ARTICLE: str = """Write a high-quality, well-structured article formatted in requested format. 
    The article should be informative, engaging, and relevant to the subject matter. 
    Use clear language, logical flow, and appropriate headings or bullet points where necessary. 
    Do not include an introduction or conclusion unrelated to the topic. 
    The article must fit entirely within the specified character limit and should follow any given 
    requirements or reference material when provided."""

    PROMPT_CREATE_IMAGE: str = """Create a picture that illustrates the content below. 
    Accurately visualize the most specific details, objects, and context. Each object must be represented 
    clearly and separately. Do not merge items unless explicitly stated.
    Requirements: do not put text, watermarks, logos, names.
    Whenever possible, do not create isolated objects or schematic diagrams. 
    For example, if the topic involves fishing equipment, show the items in a natural setting 
    like near a lake or river, rather than as a product layout on a white background. 
    The image should feel immersive and lifelike, representing the concept through a realistic scene, 
    not as a technical illustration."""
