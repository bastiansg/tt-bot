import os

import numpy as np

from langchain.embeddings import OpenAIEmbeddings

from tt_bot.meta.interfaces import TextEncoder


class OpenAIEncoder(TextEncoder):
    def __init__(self, batch_size: int = 32):
        super().__init__(batch_size)

        self.model = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    def encode(
        self,
        texts: list[str],
        contexts: list[str],
        encoder_type: str,
    ) -> np.ndarray:
        embeddings = self.model.embed_documents(texts)
        embeddings = np.array(embeddings)

        return embeddings
