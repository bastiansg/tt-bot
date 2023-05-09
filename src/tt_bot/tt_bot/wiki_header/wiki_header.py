import httpx
import random
import urllib
import asyncio

from typing import Iterable

from rich.progress import track
from tt_bot.logger import get_logger


logger = get_logger(__name__)


class WikiHeader:
    def __init__(self, max_paragraphs: int = 2, max_concurrency: int = 50):
        self.max_paragraphs = max_paragraphs
        self.max_concurrency = max_concurrency

        self.asyncio_semaphore = asyncio.Semaphore(max_concurrency)
        self.httpx_client = httpx.AsyncClient()

    async def get_header(self, wiki_title: str) -> dict:
        encoded_title = urllib.parse.quote(wiki_title)
        url = (
            "https://en.wikipedia.org/w/api.php?format=json&action=query&"
            "prop=extracts&exintro&explaintext&redirects=1&titles="
            f"{encoded_title}"
        )

        logger.info(f"url => {url}")
        async with self.asyncio_semaphore:
            response = await self.httpx_client.get(url)
            if self.asyncio_semaphore.locked():
                await asyncio.sleep(random.random())

            status_code = response.status_code
            if status_code != 200:
                logger.error(f"status code: {status_code}")
                return {}

            content = response.json()["query"]["pages"].values()
            content = list(content)[0]
            wiki_header = content.get("extract", "")
            if wiki_header:
                paragraphs = wiki_header.split("\n")
                wiki_header = " ".join(paragraphs[: self.max_paragraphs])

            return wiki_header

    async def get_headers(self, wiki_titles: Iterable[str]) -> list[str]:
        async_tasks = [
            asyncio.create_task(self.get_header(wiki_title))
            for wiki_title in track(list(wiki_titles), description="")
        ]

        wiki_headers = await asyncio.gather(*async_tasks)
        return wiki_headers
