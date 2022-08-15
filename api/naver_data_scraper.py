import asyncio
import aiohttp
from models.config import get_secret


class NaverDataScraper:
    NAVER_API_URL = "https://openapi.naver.com/v1/search"
    NAVER_API_ID = get_secret("NAVER_API_ID")
    NAVER_API_SECRET = get_secret("NAVER_API_SECRET")

    @staticmethod
    async def fetch(session, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result["items"]

    def unit_naver_url(self, category, keyword, start):
        return {
            "url": f"{self.NAVER_API_URL}/{category}?query={keyword}&display=10&start={start}",
            "headers": {
                "X-Naver-Client-Id": self.NAVER_API_ID,
                "X-Naver-Client-Secret": self.NAVER_API_SECRET,
            },
        }

    async def search(self, category, keyword, total_page):
        naver_apis = [self.unit_naver_url(category, keyword, 1 + i * 10) for i in range(total_page)]

        async with aiohttp.ClientSession() as session:
            naver_all_data = await asyncio.gather(
                *[
                    NaverDataScraper.fetch(session, api["url"], api["headers"])
                    for api in naver_apis
                ]
            )

            result = []

            for data in naver_all_data:
                if data is not None:
                    for d in data:
                        result.append(d)
            
            return result

    def run(self, category, keyword, total_page):
        return asyncio.run(self.search(category, keyword, total_page))

