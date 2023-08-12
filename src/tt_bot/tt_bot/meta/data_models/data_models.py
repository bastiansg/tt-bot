from pydantic import BaseModel, StrictStr, HttpUrl, StrictBool, NonNegativeInt


class SearchResult(BaseModel):
    title: StrictStr
    link: HttpUrl
    snippet: StrictStr
    wikipedia: StrictBool


class TextChunk(BaseModel):
    source: StrictStr
    idx: NonNegativeInt
    snippet: StrictStr
    text: StrictStr
