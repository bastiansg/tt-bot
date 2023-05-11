from langchain.utilities import GoogleSearchAPIWrapper

from tt_bot.logger import get_logger
from tt_bot.html_parsers import SimpleParser, WikiParser


logger = get_logger(__name__)


class SearchEngine:
    def __init__(self):
        self.wiki_parser = WikiParser()
        self.simple_parser = SimpleParser()
        self.search_engine = GoogleSearchAPIWrapper()

    async def search(self, query_text: str, num_results: int = 3) -> list[str]:
        results = self.search_engine.results(query_text, num_results)
        logger.info(f"results => {results}")

        wiki_results = [
            result for result in results if "Wikipedia" in result["title"]
        ]

        if not wiki_results:
            html_results = await self.simple_parser.parse_urls(results)
            return html_results

        wiki_headers = await self.wiki_parser.get_headers(wiki_results)
        return wiki_headers
