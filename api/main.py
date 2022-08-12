from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
def root():
    return {"Path": "Root"}


@app.get("/search")
def read_item(request: Request, q: str):
    print({"request": request, "q": q})

