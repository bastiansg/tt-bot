from abc import ABC, abstractmethod

from tt_bot.meta import SearchResponse


class SearchEngine(ABC):
    def __init__(self, num_results: int):
        self.num_results = num_results

    def get_extract_strategy(self, search_result_title: str) -> str:
        if "Wikipedia" in search_result_title:
            return "wikipedia"

        return "html"

    @abstractmethod
    def search(self, query_text: str, num_results: int) -> SearchResponse:
        pass
