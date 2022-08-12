from fastapi import FastAPI, Request
from models import mongodb

app = FastAPI()


@app.get("/")
def root():
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