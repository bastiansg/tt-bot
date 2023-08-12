import numpy as np

from langchain.embeddings import OpenAIEmbeddings

from tt_bot.cache import cache
from tt_bot.meta import TextEncoder, TextChunk


class OpenAIEncoder(TextEncoder):
    def __init__(self):
        self.model = OpenAIEmbeddings()

    @cache
    def encode(self, text_chunks: list[TextChunk]) -> np.ndarray:
        texts = [tc.text for tc in text_chunks]
        embeddings = self.model.embed_documents(texts)
        embeddings = np.array(embeddings)

        return embeddings
