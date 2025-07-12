from fastapi import FastAPI

from app.models import Article


app = FastAPI()


# Endpoints:
## create-article [POST]
### Input:
##### Topic : str (required, topic of the article)
##### Length : int (required, maximum amount of characters in the article)
##### Requirements: str (optional, extra requirements)
##### Reference: str (optional, reference for the article)
##### Output format: str ("markdown" by default, "html")

### Output:
##### Text: str (text of the article in HTML format)

## create-image [POST]
### Input:
##### Description : str (required, description of the image)
##### Width: int
##### Height: int
##### Requirements: str (optional, extra requirements)

### Output:
##### Image URL (Amazon W3)

## illustrate-article
### Input:
##### Text: str (text of the article in markdown or html format)
##### Max images: int (maximum amount of images)

### Output
##### Text : str (text of the article in markdown or html format, with pictures)


@app.post("/create-article")
async def create_article(article: Article):
    return article
