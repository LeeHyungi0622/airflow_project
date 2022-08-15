from data_scraper import DataScraper
from fastapi import FastAPI, Request
from models import mongodb
from models.cafe import CafeModel

from datetime import datetime

app = FastAPI()


@app.get("/")
async def root():
    cafe = CafeModel(cafename="cafename1", contents="contents1", datetime="datetime1", title="title1", url="url1") 
    await mongodb.engine.save(cafe)
    return {"Path": "Root"}


@app.get("/search")
async def read_item(request: Request):
    # 1. 쿼리에서 검색어 추출
    keyword = "데이터 엔지니어"
    # 2. 데이터 수집기로 해당 검색어에 대해 데이터를 수집
    data_scrapper = DataScraper()
    naver_cafe = await data_scrapper.search('cafearticle.json', keyword, 3)
    kakao_cafe = await data_scrapper.search('cafe', keyword, 3)

    total_result = naver_cafe + kakao_cafe
    print(total_result)

    cafe_models = []
    for cafe in total_result:
        print(cafe)
        try:
            cafe_model = CafeModel(
                cafename=cafe["cafename"],
                contents=cafe["description"],
                datetime=datetime.now(),
                title=cafe["title"],
                url=cafe["cafeurl"] 
            )
        except KeyError:
            cafe_model = CafeModel(
                cafename=cafe["cafename"],
                contents=cafe["contents"],
                datetime=datetime.now(),
                title=cafe["title"],
                url=cafe["url"] 
            )
        cafe_models.append(cafe_model)
    await mongodb.engine.save_all(cafe_models)
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
