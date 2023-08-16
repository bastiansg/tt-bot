import requests

from bs4 import BeautifulSoup

from itertools import islice
from more_itertools import flatten

from tt_bot.cache import cache
from tt_bot.logger import get_logger
from tt_bot.meta import SearchResponse, WebExtractor, TextChunk


logger = get_logger(__name__)


class HTMLExtractor(WebExtractor):
    def __init__(
        self,
        max_elements: int = 50,
        min_paragraph_words: int = 10,
        find_elements: list[str] = ["p"],
    ):
        super().__init__()

        self.max_elements = max_elements
        self.min_paragraph_words = min_paragraph_words
        self.find_elements = find_elements

    def text_normalize(self, text: str) -> str:
        text = text.replace("\xa0", " ")
        text = text.strip()

        return text

    @cache
    def extract(self, search_result: SearchResponse) -> list[TextChunk]:
        link = search_result.link

        try:
            response = requests.get(link, timeout=5)
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

        paragraphs = (p.text.split("\n") for p in next(found_elements))
        paragraphs = map(self.text_normalize, flatten(paragraphs))
        paragraphs = (
            p for p in paragraphs if len(p.split()) >= self.min_paragraph_words
        )

        paragraphs = islice(paragraphs, self.max_paragraphs)
        snippet = search_result.snippet
        text_chunks = [
            TextChunk(
                source=link,
                idx=idx,
                text=p,
                snippet=snippet,
            )
            for idx, p in enumerate(paragraphs, start=1)
        ]

        logger.info(f"text_chunks => {len(text_chunks)}")
        return text_chunks
