from naver_data_scraper import NaverDataScraper
from kakao_data_scraper import KakaoDataScraper
from fastapi import FastAPI, Request
from models import mongodb
from models.cafe import CafeModel

from datetime import datetime

app = FastAPI()


@app.get("/")
async def root():
    return {"Path": "Root"}


@app.get("/search/naver")
async def read_item_from_naver(request: Request):
    keyword = "데이터 엔지니어"
    
    naver_data_scrapper = NaverDataScraper()
    naver_cafe_result = await naver_data_scrapper.search('cafearticle.json', keyword, 3)

    cafe_models = []
    for item in naver_cafe_result:
        cafe_model = CafeModel(
            cafename=item["cafename"],
            contents=item["description"],
            datetime=datetime.now(),
            title=item["title"],
            url=item["cafeurl"] 
        )
        cafe_models.append(cafe_model)
    result = await mongodb.engine.save_all(cafe_models)
    return {"result": result}

@app.get("/search/kakao")
async def read_item_from_kakao(request: Request):
    keyword = "데이터 엔지니어"
    kakao_data_scrapper = KakaoDataScraper()
    kakao_cafe_result = await kakao_data_scrapper.search('cafe', keyword, 3)

    cafe_models = []
    for item in kakao_cafe_result:
        cafe_model = CafeModel(
            cafename=item["cafename"],
            contents=item["contents"],
            datetime=datetime.now(),
            title=item["title"],
            url=item["url"] 
        )
        cafe_models.append(cafe_model)
    result = await mongodb.engine.save_all(cafe_models)
    return {"result": result}


@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    mongodb.close()
