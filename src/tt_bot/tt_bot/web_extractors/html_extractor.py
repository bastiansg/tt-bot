import requests

from bs4 import BeautifulSoup
from more_itertools import flatten

from tt_bot.cache import cache
from tt_bot.logger import get_logger
from tt_bot.meta import SearchResult, WebExtractor, TextChunk


logger = get_logger(__name__)


class HTMLExtractor(WebExtractor):
    def __init__(
        self,
        find_elements: list[str] = ["p"],
        max_concurrency: int = 50,
        max_elements: int = 5,
    ):
        super().__init__()

        self.find_elements = find_elements
        self.max_concurrency = max_concurrency
        self.max_elements = max_elements

    def text_normalize(self, text: str) -> str:
        text = text.replace("\xa0", " ")
        text = text.strip()

        return text

    @cache
    def extract(self, search_result: SearchResult) -> list[TextChunk]:
        link = search_result.link

        try:
            response = requests.get(link)
        except Exception as err:
            logger.error(err)
            return []

        status_code = response.status_code
        if status_code != 200:
            logger.error(f"status code: {status_code}")
            return []

        soup = BeautifulSoup(response.content, features="html.parser")
        found_elements = (
            soup.find_all(find_element, limit=self.max_elements)
            for find_element in self.find_elements
        )

        snippet = search_result.snippet
        text_chunks = [
            TextChunk(
                source=link,
                idx=idx,
                text=self.text_normalize(element.text),
                snippet=snippet,
            )
            for idx, element in enumerate(flatten(found_elements))
        ]

        return text_chunks
