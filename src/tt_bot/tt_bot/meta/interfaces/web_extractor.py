import asyncio

from more_itertools import flatten
from abc import ABC, abstractmethod

from tt_bot.meta import SearchResponse, TextChunk


class WebExtractor(ABC):
    def __init__(self, max_paragraphs: int = 5, max_concurrency=10):
        self.max_paragraphs = max_paragraphs
        self.asyncio_semaphore = asyncio.Semaphore(max_concurrency)

    @abstractmethod
    def extract(
        self,
        search_result: SearchResponse,
    ) -> list[TextChunk]:
        pass

    async def async_extract(
        self,
        search_result: SearchResponse,
    ) -> list[TextChunk]:
        async with self.asyncio_semaphore:
            return await asyncio.to_thread(self.extract, search_result)

    async def extract_search_results(
        self,
        search_results: list[SearchResponse],
    ) -> list[TextChunk]:
        async_tasks = (self.async_extract(result) for result in search_results)

        search_results = await asyncio.gather(*async_tasks)
        search_results = list(flatten(search_results))

        return search_results
