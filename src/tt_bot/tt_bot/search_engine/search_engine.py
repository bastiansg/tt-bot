from more_itertools import flatten
from langchain.utilities import GoogleSearchAPIWrapper

from tt_bot.logger import get_logger
from tt_bot.wiki_header import WikiHeader
from tt_bot.html_parser import HTMLParser


logger = get_logger(__name__)


class SearchEngine:
    def __init__(self, num_results: int = 3):
        self.num_results = num_results

        self.wiki_header = WikiHeader()
        self.html_parser = HTMLParser()
        self.search_engine = GoogleSearchAPIWrapper()

    async def search(self, query_text: str) -> list[str]:
        results = self.search_engine.results(query_text, self.num_results)
        logger.info(f"results => {results}")

        wiki_results = [
            result for result in results if "Wikipedia" in result["title"]
        ]

        if not wiki_results:
            urls = (result["link"] for result in results)
            html_texts = await self.html_parser.parse_urls(urls)
            html_texts = list(flatten(html_texts))

            return html_texts

        wiki_titles = (
            wiki_result["title"].split(" - ")[0]
            for wiki_result in wiki_results
        )

        wiki_headers = await self.wiki_header.get_headers(wiki_titles)
        return wiki_headers
