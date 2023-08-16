import regex
import urllib
import requests

from itertools import islice

from tt_bot.cache import cache
from tt_bot.logger import get_logger
from tt_bot.meta import SearchResponse, WebExtractor, TextChunk


logger = get_logger(__name__)


class WikiExtractor(WebExtractor):
    def __init__(
        self,
        lang_pattern: str = r"(https:\/\/)(.*)(.wikipedia.org)",
        clean_pattern: str = r"\[\d{1,}\]\u200b",
    ):
        super().__init__()

        self.lang_pattern = regex.compile(lang_pattern)
        self.clean_pattern = regex.compile(clean_pattern)

    def parse_paragraph(self, pargraph: str) -> str:
        pargraph = self.clean_pattern.sub(" ", pargraph)
        pargraph = " ".join(pargraph.split())
        pargraph = pargraph.strip()

        return pargraph

    @cache
    def extract(self, search_result: SearchResponse) -> list[TextChunk]:
        link = search_result.link
        lang = self.lang_pattern.search(link).groups()[1]
        wiki_title = search_result.title.split(" - ")[0]

        encoded_title = urllib.parse.quote(wiki_title)
        wiki_header_url = (
            f"https://{lang}.wikipedia.org/w/api.php?format=json&action=query&"
            "prop=extracts&exintro&explaintext&redirects=1&titles="
            f"{encoded_title}"
        )

        logger.debug(f"wiki_header_url => {wiki_header_url}")
        response = requests.get(wiki_header_url)

        status_code = response.status_code
        if status_code != 200:
            logger.error(f"status code: {status_code}")
            return {}

        content = response.json()["query"]["pages"].values()
        content = list(content)[0]
        wiki_header = content.get("extract", "")
        if not wiki_header:
            return []

        paragraphs = wiki_header.split("\n")
        paragraphs = (self.parse_paragraph(p) for p in paragraphs)
        paragraphs = islice(paragraphs, self.max_paragraphs)

        snippet = search_result.snippet
        text_chunks = [
            TextChunk(
                idx=idx,
                source=link,
                text=p,
                snippet=snippet,
            )
            for idx, p in enumerate(paragraphs, start=1)
        ]

        return text_chunks
