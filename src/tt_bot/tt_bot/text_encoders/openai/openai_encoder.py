import numpy as np

from langchain.embeddings import OpenAIEmbeddings

from tt_bot.cache import cache
from tt_bot.meta import TextEncoder


class OpenAIEncoder(TextEncoder):
    def __init__(self):
        self.model = OpenAIEmbeddings()

    @cache
    def encode(self, texts: list[str]) -> np.ndarray:
        embeddings = self.model.embed_documents(texts)
        embeddings = np.array(embeddings)

        return embeddings
