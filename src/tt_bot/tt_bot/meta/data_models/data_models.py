from typing import Optional
from pydantic import (
    validator,
    BaseModel,
    StrictStr,
    HttpUrl,
    NonNegativeInt,
    PositiveInt,
    StrictFloat,
)


EXTRACT_STRATEGIES = [
    "html",
    "wikipedia",
]


class SearchResponse(BaseModel):
    title: StrictStr
    link: HttpUrl
    snippet: StrictStr
    extract_strategy: StrictStr

    @validator("extract_strategy")
    def extract_strategy_validator(cls, v):
        if v not in EXTRACT_STRATEGIES:
            raise ValueError(
                f"Invalid extract_strategy: {v},"
                "extract_strategy must be one of the following strings:"
                f" {EXTRACT_STRATEGIES}"
            )

        return v


class TextChunk(BaseModel):
    source: StrictStr
    idx: NonNegativeInt
    snippet: StrictStr
    text: StrictStr


class QAResponse(BaseModel):
    answer: Optional[StrictStr]


class RetrievalResponse(BaseModel):
    source: StrictStr
    texts: list[StrictStr]
    similarity: StrictFloat
    relevance: PositiveInt

    @validator("similarity")
    def similarity_validator(cls, v):
        if v < 0.0 or v > 1.0:
            raise ValueError(
                f"Invalid similarity: {v},"
                "similarity must be in the range [0, 1]"
            )

        return v
