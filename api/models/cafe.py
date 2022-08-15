from datetime import datetime
from odmantic import Model
from typing import Optional

class CafeModel(Model):
    cafename: Optional[str] = None
    contents: Optional[str] = None
    datetime: datetime
    title: Optional[str] = None
    url: Optional[str] = None

    class Config:
        collection = "cafe"