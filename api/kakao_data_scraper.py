import asyncio
import aiohttp
from models.config import get_secret


class KakaoDataScraper:
    KAKAO_API_URL = "https://dapi.kakao.com/v2/search"
    KAKAO_AUTH = get_secret("KAKAO_AUTH")

    @staticmethod
    async def fetch(session, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result["documents"]

    def unit_kakao_url(self, category, keyword, page):
        return {
            "url": f"{self.KAKAO_API_URL}/{category}?query={keyword}&size=10&page={page}",
            "headers": {
                "Authorization": self.KAKAO_AUTH
            }
        }

    async def search(self, category, keyword, total_page):
        kakao_apis = [self.unit_kakao_url(category, keyword, i) for i in range(1, total_page + 1)]

        async with aiohttp.ClientSession() as session:

            kakao_all_data = await asyncio.gather(
                *[
                    KakaoDataScraper.fetch(session, api["url"], api["headers"])
                    for api in kakao_apis
                ]
            )

            result = []

            for data in kakao_all_data:
                if data is not None:
                    for d in data:
                        result.append(d)
            return result

    def run(self, category, keyword, total_page):
        return asyncio.run(self.search(category, keyword, total_page))

