from typing import Optional
from pydantic import BaseModel


class Article(BaseModel):
    topic: str
    length: int = 1000
    requirements: Optional[str] = None
    reference: Optional[str] = None
    output_format: str = "html"
    result: Optional[str] = None


class Image(BaseModel):
    description: str
    width: int = 1024
    height: int = 1024
    amazon_s3_bucket: str
    amazon_s3_path: str
    requirements: Optional[str] = None
    reference: Optional[str] = None
    quality: str = "hd"
    url: Optional[str] = None
