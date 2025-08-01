import os
import shutil
import requests
import time
from fastapi import FastAPI, Depends, APIRouter

from app.config import Config
from app.models import Article, Image
from app.modules.auth.token import verify_token
from app.modules.deepseek.client import DeepseekClient
from app.modules.openai.client import OpenAIClient
from app.modules.amazon_s3.client import AmazonS3Client


app: FastAPI = FastAPI()
deepseek_client: DeepseekClient = DeepseekClient()
openai_client: OpenAIClient = OpenAIClient()
amazon_s3_client: AmazonS3Client = AmazonS3Client()


api_v1_router = APIRouter(
    prefix="/api/v1",
    dependencies=[Depends(verify_token)]
)


@app.get("/")
async def root() -> dict:
    return {"message": "Welcome to the AI Content Generation API"}


@api_v1_router.post("/create-article")
async def create_article(article: Article) -> Article:
    prompt: str = Config.PROMPT_CREATE_ARTICLE
    if article.requirements:
        prompt += f"\nRequirements: {article.requirements}"

    if article.reference:
        prompt += f"\nReference: {article.reference}"

    if article.output_format == "html":
        prompt += """Format the output in HTML, but include only content-level tags 
        such as <h2>, <p>, <ul>, <li>, <strong>, etc.
        Do not include <html>, <head>, <body>, or any global document tags."""
    elif article.output_format:
        prompt += f"\nOutput format: {article.output_format}"

    article.result = deepseek_client.request(
        prompt=prompt,
        task=f"Topic for the article: {article.topic}, maximum characters amount: {article.length}",
    )

    if article.output_format == "html":
        article.result = article.result.replace("\n", "")

    return article


@api_v1_router.post("/create-image")
async def create_image(image: Image) -> Image:
    response_image_url: str = openai_client.request(
        prompt=Config.PROMPT_CREATE_IMAGE,
        task=image.description,
        width=image.width,
        height=image.height,
        quality=image.quality,
    )

    file_name: str = f"{str(time.time()).replace('.', '')}.jpg"
    local_path: str = os.path.join(Config.AWS_LOCAL_TMP_DIR, file_name)
    os.makedirs(Config.AWS_LOCAL_TMP_DIR, exist_ok=True)

    img: requests.Response = requests.get(response_image_url)
    with open(local_path, "wb") as file:
        file.write(img.content)

    image.url = amazon_s3_client.upload_image(
        local_path,
        image.amazon_s3_bucket,
        image.amazon_s3_path + file_name,
    )

    if os.path.exists(local_path):
        os.remove(local_path)

    if os.path.exists(Config.AWS_LOCAL_TMP_DIR):
        shutil.rmtree(Config.AWS_LOCAL_TMP_DIR)

    return image


app.include_router(api_v1_router)
