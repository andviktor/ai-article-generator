from pydantic import BaseModel


class Article(BaseModel):
    topic: str
    length: int = 1000
    requirements: str | None = None
    reference: str | None = None
    output_format: str = "html"
    result: str | None = None


class Image(BaseModel):
    description: str
    width: int = 1024
    height: int = 1024
    amazon_s3_bucket: str
    amazon_s3_path: str
    requirements: str | None = None
    reference: str | None = None
    quality: str = "hd"
    url: str | None = None
