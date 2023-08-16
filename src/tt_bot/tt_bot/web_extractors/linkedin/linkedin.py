import os
import regex

from linkedin_api import Linkedin

from tt_bot.cache import cache
from tt_bot.logger import get_logger
from tt_bot.utils.json_data import get_pretty
from tt_bot.meta import SearchResponse, WebExtractor, TextChunk


from .parsers import parse_person_profile, parse_company_profile


logger = get_logger(__name__)


class LinkedinExtractor(WebExtractor):
    def __init__(
        self,
        person_pattern: str = r"https:\/\/(www|[a-z]{2})\.linkedin\.com\/in\/",  # noqa
        company_pattern: str = r"https:\/\/(www|[a-z]{2})\.linkedin\.com\/company\/",  # noqa
    ):
        super().__init__()
        self.linkedin_api = Linkedin(
            os.environ["LINKEDIN_EMAIL"],
            os.environ["LINKEDIN_PASSWROD"],
        )

        self.person_pattern = regex.compile(person_pattern)
        self.company_pattern = regex.compile(company_pattern)

    @cache
    def extract(self, search_result: SearchResponse) -> list[TextChunk]:
        link = search_result.link
        public_id = link.split("/")[-1]

        result = ""
        if self.person_pattern.match(link):
            result = self.linkedin_api.get_profile(public_id)
            result = parse_person_profile(result)

        if self.company_pattern.match(link):
            result = self.linkedin_api.get_company(public_id)
            result = parse_company_profile(result)

        assert result, f"Unreconized linkedin url pattern => {link}"

        logger.info(link)
        logger.info(result)
        snippet = search_result.snippet
        text_chunks = [
            TextChunk(
                idx=1,
                source=link,
                text=get_pretty(result),
                snippet=snippet,
            )
        ]

        return text_chunks
