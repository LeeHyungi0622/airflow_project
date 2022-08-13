from ast import keyword
from fastapi import FastAPI, Request
from models import mongodb
from models.book import BookModel

app = FastAPI()


@app.get("/")
async def root():
    book = BookModel(keyword="HG", publisher="HGPublic", price=1200, image="hyungi.png")
    await mongodb.engine.save(book)
    return {"Path": "Root"}


@app.get("/search")
def read_item(request: Request, q: str):
    print({"request": request, "q": q})


@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    mongodb.close()
