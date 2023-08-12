import numpy as np

from abc import ABC, abstractmethod

from tt_bot.meta import TextChunk


class TextEncoder(ABC):
    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def encode(self, text_chunks: list[TextChunk]) -> np.ndarray:
        pass
