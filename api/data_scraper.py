import asyncio
import aiohttp
from models.config import get_secret


class DataScraper:
    NAVER_API_URL = "https://openapi.naver.com/v1/search"
    NAVER_API_ID = get_secret("NAVER_API_ID")
    NAVER_API_SECRET = get_secret("NAVER_API_SECRET")

    KAKAO_API_URL = "https://dapi.kakao.com/v2/search"
    KAKAO_AUTH = get_secret("KAKAO_AUTH")

    @staticmethod
    async def fetch(session, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                if 'naver' in url:
                    return result["items"]
                elif 'kakao' in url:
                    return result["documents"]

    def unit_naver_url(self, category, keyword, start):
        return {
            "url": f"{self.NAVER_API_URL}/{category}?query={keyword}&display=10&start={start}",
            "headers": {
                "X-Naver-Client-Id": self.NAVER_API_ID,
                "X-Naver-Client-Secret": self.NAVER_API_SECRET,
            },
        }

    def unit_kakao_url(self, category, keyword, page):
        return {
            "url": f"{self.KAKAO_API_URL}/{category}?query={keyword}&size=10&page={page}",
            "headers": {
                "Authorization": self.KAKAO_AUTH
            }
        }

    async def search(self, category, keyword, total_page):
        naver_apis = [self.unit_naver_url(category, keyword, 1 + i * 10) for i in range(total_page)]
        kakao_apis = [self.unit_kakao_url(category, keyword, i) for i in range(1, total_page + 1)]

        async with aiohttp.ClientSession() as session:
            naver_all_data = await asyncio.gather(
                *[
                    DataScraper.fetch(session, api["url"], api["headers"])
                    for api in naver_apis
                ]
            )


            kakao_all_data = await asyncio.gather(
                *[
                    DataScraper.fetch(session, api["url"], api["headers"])
                    for api in kakao_apis
                ]
            )

            result = []

            for data in naver_all_data:
                if data is not None:
                    for d in data:
                        result.append(d)
            
            for data in kakao_all_data:
                if data is not None:
                    for d in data:
                        result.append(d)
            return result

    def run(self, category, keyword, total_page):
        return asyncio.run(self.search(category, keyword, total_page))


if __name__ == "__main__":
    scraper = NaverDataScraper()
    print(scraper.run("book", "파이썬", 3))
    print(len(scraper.run("book", "파이썬", 3)))
