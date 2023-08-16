import numpy as np

from langchain.embeddings import OpenAIEmbeddings

from tt_bot.cache import cache
from tt_bot.meta import TextEncoder
from tt_bot.logger import get_logger


logger = get_logger(__name__)


class OpenAIEncoder(TextEncoder):
    def __init__(self):
        self.model = OpenAIEmbeddings()

    @cache
    def encode(self, texts: list[str]) -> np.ndarray:
        embeddings = self.model.embed_documents(texts)
        embeddings = np.array(embeddings)

        logger.info(f"embeddings => {embeddings.shape}")
        return embeddings
