from pydantic import BaseModel


class Article(BaseModel):
    topic: str
    length: int
    requirements: str | None = None
    reference: str | None = None
    output_format: str = "markdown" # markdown, html
    result: str | None = None
