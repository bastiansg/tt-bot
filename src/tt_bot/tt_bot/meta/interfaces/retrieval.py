from abc import ABC, abstractmethod

from tt_bot.meta import (
    SearchEngine,
    TextEncoder,
    WebExtractor,
    RetrievalResponse,
)


class Retrieval(ABC):
    def __init__(
        self,
        search_engine: SearchEngine,
        text_encoder: TextEncoder,
        extractors: dict[str, WebExtractor],
        sim_tresh: float = 0.8,
        top_k: int = 3,
    ):
        self.search_engine = search_engine
        self.text_encoder = text_encoder
        self.extractors = extractors

        self.sim_tresh = sim_tresh
        self.top_k = top_k

    @abstractmethod
    async def retrieve(self, query_text: str) -> list[RetrievalResponse]:
        pass
