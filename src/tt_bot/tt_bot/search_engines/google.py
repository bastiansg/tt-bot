from langchain.utilities import GoogleSearchAPIWrapper

from tt_bot.cache import cache
from tt_bot.logger import get_logger
from tt_bot.meta import SearchEngine, SearchResponse


logger = get_logger(__name__)


class GoogleSearchEngine(SearchEngine):
    def __init__(self, num_results: int = 3):
        super().__init__(num_results=num_results)
        self.search_engine = GoogleSearchAPIWrapper()

    @cache
    def search(self, query_text: str) -> list[SearchResponse]:
        results = self.search_engine.results(query_text, self.num_results)
        if (
            results[0].get("Result")
            == "No good Google Search Result was found"
        ):
            logger.info("No google results")
            return []

        logger.info(f"search_engine_results => {results}")
        search_results = [
            SearchResponse(
                title=result["title"],
                link=result["link"],
                snippet=result["snippet"],
                link_type=self.get_link_type(result["link"]),
            )
            for result in results
        ]

        return search_results
