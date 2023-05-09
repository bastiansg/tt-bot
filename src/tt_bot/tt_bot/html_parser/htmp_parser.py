import httpx
import random
import asyncio

from typing import Iterator
from bs4 import BeautifulSoup
from rich.progress import track
from more_itertools import flatten

from tt_bot.logger import get_logger


logger = get_logger(__name__)


class HTMLParser:
    def __init__(
        self,
        find_elements: list[str] = ["p"],
        min_words: int = 20,
        max_concurrency: int = 50,
    ):
        self.find_elements = find_elements
        self.min_words = min_words
        self.max_concurrency = max_concurrency

        self.asyncio_semaphore = asyncio.Semaphore(max_concurrency)
        self.httpx_client = httpx.AsyncClient()

    def parse_found_text(self, text: str) -> str:
        text = text.replace("\xa0", " ")
        text = text.strip()

        return text

    def filter_found_text(self, text: str) -> bool:
        if not text:
            return False

        if len(text.split()) < self.min_words:
            return False

        return True

    async def parse_url(self, url: str) -> list[str]:
        async with self.asyncio_semaphore:
            response = await self.httpx_client.get(url)
            if self.asyncio_semaphore.locked():
                await asyncio.sleep(random.random())

            status_code = response.status_code
            if status_code != 200:
                logger.error(f"status code: {status_code}")
                return []

            soup = BeautifulSoup(response.content, features="html.parser")
            found_elements = (
                soup.findAll(find_element)
                for find_element in self.find_elements
            )

            texts = (
                self.parse_found_text(element.text)
                for element in flatten(found_elements)
            )

            texts = [text for text in texts if self.filter_found_text(text)]
            return texts

    async def parse_urls(self, urls: Iterator[str]) -> list[list[str]]:
        async_tasks = [
            asyncio.create_task(self.parse_url(url))
            for url in track(list(urls), description="")
        ]

        url_texts = await asyncio.gather(*async_tasks)
        return url_texts
