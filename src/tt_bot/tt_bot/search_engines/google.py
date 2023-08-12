from langchain.utilities import GoogleSearchAPIWrapper

from tt_bot.cache import cache
from tt_bot.logger import get_logger
from tt_bot.meta import SearchResult


logger = get_logger(__name__)


class GoogleSearchEngine:
    def __init__(self):
        self.search_engine = GoogleSearchAPIWrapper()

    @cache
    def search(
        self,
        query_text: str,
        num_results: int = 3,
    ) -> list[SearchResult]:
        results = self.search_engine.results(query_text, num_results)
        if (
            results[0].get("Result")
            == "No good Google Search Result was found"
        ):
            logger.info("No google results")
            return []

        search_results = [
            SearchResult(
                title=result["title"],
                link=result["link"],
                snippet=result["snippet"],
                wikipedia=True if "Wikipedia" in result["title"] else False,
            )
            for result in results
        ]

        return search_results
