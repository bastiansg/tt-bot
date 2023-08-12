import asyncio

from rich.progress import track
from more_itertools import flatten
from abc import ABC, abstractmethod

from tt_bot.meta import SearchResult, TextChunk


class WebExtractor(ABC):
    def __init__(self, max_concurrency=10):
        self.asyncio_semaphore = asyncio.Semaphore(max_concurrency)

    @abstractmethod
    def extract(
        self,
        search_result: SearchResult,
    ) -> list[TextChunk]:
        pass

    async def async_extract(
        self,
        search_result: SearchResult,
    ) -> list[TextChunk]:
        async with self.asyncio_semaphore:
            return await asyncio.to_thread(self.extract, search_result)

    async def extract_search_results(
        self,
        search_results: list[SearchResult],
    ) -> list[TextChunk]:
        async_tasks = (
            self.async_extract(result)
            for result in track(
                list(search_results),
                description="",
            )
        )

        search_results = await asyncio.gather(*async_tasks)
        search_results = list(flatten(search_results))

        return search_results
