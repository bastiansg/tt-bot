import httpx
import random
import asyncio

from typing import Iterator
from bs4 import BeautifulSoup
from rich.progress import track
from more_itertools import flatten

from tt_bot.logger import get_logger


logger = get_logger(__name__)


class SimpleParser:
    def __init__(
        self,
        find_elements: list[str] = ["p"],
        max_concurrency: int = 50,
        max_elements: int = 5,
    ):
        self.find_elements = find_elements
        self.max_concurrency = max_concurrency
        self.max_elements = max_elements

        self.asyncio_semaphore = asyncio.Semaphore(max_concurrency)
        self.httpx_client = httpx.AsyncClient()

    def parse_found_text(self, text: str) -> str:
        text = text.replace("\xa0", " ")
        text = text.strip()

        return text

    def filter_found_text(self, text: str) -> bool:
        if not text:
            return False

        return True

    async def parse_url(self, result: dict) -> Iterator[dict]:
        async with self.asyncio_semaphore:
            link = result["link"]
            try:
                response = await self.httpx_client.get(link)
            except Exception as err:
                logger.error(err)
                return []

            if self.asyncio_semaphore.locked():
                await asyncio.sleep(random.random())

            status_code = response.status_code
            if status_code != 200:
                logger.error(f"status code: {status_code}")
                return []

            soup = BeautifulSoup(response.content, features="html.parser")
            found_elements = (
                soup.find_all(find_element, limit=self.max_elements)
                for find_element in self.find_elements
            )

            texts = (
                self.parse_found_text(element.text)
                for element in flatten(found_elements)
            )

            snippet = result["snippet"]
            html_results = (
                {
                    "link": link,
                    "text": f"{snippet} {text}",
                }
                for text in texts
                if self.filter_found_text(text)
            )

            return html_results

    async def parse_urls(self, results: Iterator[dict]) -> list[dict]:
        async_tasks = [
            asyncio.create_task(self.parse_url(result))
            for result in track(list(results), description="")
        ]

        html_results = await asyncio.gather(*async_tasks)
        html_results = list(flatten(html_results))

        return html_results
