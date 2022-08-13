from ast import keyword
from odmantic import Model
from typing import Optional


class BookModel(Model):
    keyword: Optional[str] = None
    publisher: Optional[str] = None
    price: Optional[int] = None
    image: Optional[str] = None

    class Config:
        collection = "books"


# db fastapi-pj => collection books => document {
# keyword: 'python'
# publisher: 'bj_public'
# }
