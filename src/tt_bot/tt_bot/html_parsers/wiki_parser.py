import regex
import httpx
import random
import urllib
import asyncio

from typing import Iterable

from rich.progress import track
from tt_bot.logger import get_logger


logger = get_logger(__name__)


class WikiParser:
    def __init__(
        self,
        max_paragraphs: int = 2,
        max_concurrency: int = 50,
        lang_pattern: str = r"(https:\/\/)(.*)(.wikipedia.org)",
        clean_pattern: str = r"\[\d{1,}\]\u200b",
    ):
        self.max_paragraphs = max_paragraphs
        self.max_concurrency = max_concurrency

        self.asyncio_semaphore = asyncio.Semaphore(max_concurrency)
        self.httpx_client = httpx.AsyncClient()
        self.lang_pattern = regex.compile(lang_pattern)
        self.clean_pattern = regex.compile(clean_pattern)

    def parse_paragraph(self, pargraph: str) -> str:
        pargraph = self.clean_pattern.sub(" ", pargraph)
        pargraph = " ".join(pargraph.split())
        pargraph = pargraph.strip()

        return pargraph

    async def get_header(self, wiki_result: dict) -> dict:
        link = wiki_result["link"]
        lang = self.lang_pattern.search(link).groups()[1]
        wiki_title = wiki_result["title"].split(" - ")[0]

        encoded_title = urllib.parse.quote(wiki_title)
        url = (
            f"https://{lang}.wikipedia.org/w/api.php?format=json&action=query&"
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
                paragraphs = [self.parse_paragraph(p) for p in paragraphs]
                wiki_header = {
                    "text": " ".join(paragraphs[: self.max_paragraphs]),
                    "link": link,
                }

            return wiki_header

    async def get_headers(self, wiki_results: Iterable[dict]) -> list[dict]:
        async_tasks = [
            asyncio.create_task(self.get_header(wiki_result))
            for wiki_result in track(list(wiki_results), description="")
        ]

        wiki_headers = await asyncio.gather(*async_tasks)
        return wiki_headers
