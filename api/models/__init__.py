from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from .config import get_secret


class MongoDB:
    MONGO_DB_NAME = get_secret("MONGO_DB_NAME")
    MONGO_URL = get_secret("MONGO_URL")
    def __init__(self):
        self.client = None
        self.engine = None

    def connect(self):
        self.client = AsyncIOMotorClient(self.MONGO_URL)
        self.engine = AIOEngine(motor_client=self.client, database=self.MONGO_DB_NAME)
        print("DB와 성공적으로 연결되었습니다.")

    def close(self):
        self.client.close()


mongodb = MongoDB()
