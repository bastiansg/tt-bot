import numpy as np

from abc import abstractmethod
from rich.progress import track
from itertools import zip_longest
from more_itertools import chunked, flatten


class TextEncoder:
    def __init__(self, batch_size: int):
        self.batch_size = batch_size

    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def encode(
        self,
        texts: list[str],
        contexts: list[str],
        encoder_type: str = "",
    ) -> np.ndarray:
        raise NotImplementedError

    def batch_encode(
        self,
        texts: list[str],
        contexts: list[str],
        encoder_type: str = "",
    ) -> np.ndarray:
        text_chunks = chunked(texts, self.batch_size)
        context_chunks = chunked(contexts, self.batch_size)
        total = len(texts) // self.batch_size
        embeddings = (
            self.encode(text_chunk, context_chunk, encoder_type)
            for text_chunk, context_chunk in track(
                zip_longest(text_chunks, context_chunks),
                total=total,
                description="",
            )
        )

        embeddings = np.array(list(flatten(embeddings)))
        return embeddings
