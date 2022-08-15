from naver_data_scraper import NaverDataScraper
from fastapi import FastAPI, Request
from models import mongodb
from models.book import BookModel

app = FastAPI()


@app.get("/")
async def root():
    return {"Path": "Root"}


@app.get("/search")
async def read_item(request: Request, q: str):
    print({"request": request, "q": q})
    # 1. 쿼리에서 검색어 추출
    keyword = q
    # 2. 데이터 수집기로 해당 검색어에 대해 데이터를 수집
    naver_data_scrapper = NaverDataScraper()
    books = await naver_data_scrapper.search('book', keyword, 3)
    print(books)
    book_models = []
    for book in books:
        print(book)
        book_model = BookModel(
            keyword=keyword,
            publisher=book["publisher"],
            discount=book["discount"],
            image=book["image"],
        )
        book_models.append(book_model)
    await mongodb.engine.save_all(book_models)
    return {"result": "success"}
    # 3. DB에 수집된 데이터 저장
    # - 수집된 각각의 데이터에 대해서 DB에 들어갈 모델 인스턴스를 찍는다.
    # - 각 모델 인스턴스를 DB에 저장한다.


@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    mongodb.close()
