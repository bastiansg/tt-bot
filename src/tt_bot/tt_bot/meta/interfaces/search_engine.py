import regex

from abc import ABC, abstractmethod

from tt_bot.meta import SearchResponse


class SearchEngine(ABC):
    def __init__(
        self,
        num_results: int,
        wiki_pattern: str = r"https:\/\/([a-z]{2})\.wikipedia\.org\/wiki\/",
        linkedin_pattern: str = r"https:\/\/([a-z]{2,3})\.linkedin\.com\/(in|company)\/",  # noqa
    ):
        self.num_results = num_results
        self.wiki_pattern = regex.compile(wiki_pattern)
        self.linkedin_pattern = regex.compile(linkedin_pattern)

    def get_link_type(self, search_result_link: str) -> str:
        if self.wiki_pattern.match(search_result_link):
            return "wikipedia"

        if self.linkedin_pattern.match(search_result_link):
            return "linkedin"

        return "html"

    @abstractmethod
    def search(self, query_text: str, num_results: int) -> SearchResponse:
        pass
