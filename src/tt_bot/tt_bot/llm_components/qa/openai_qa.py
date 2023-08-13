import json

from json import JSONDecodeError
from pydantic import ValidationError


from tt_bot.logger import get_logger
from tt_bot.utils.json_data import get_pretty
from tt_bot.exceptions import LLMResponseError
from tt_bot.meta import OpenAIChatLLM, QAResponse


logger = get_logger(__name__)


class OpenAIQA(OpenAIChatLLM):
    def __init__(self, conf_path: str = "/resources/conf/openai-qa.yaml"):
        super().__init__(conf_path=conf_path)

    async def async_generate(
        self,
        text_chunks: list[str],
        question: str,
    ) -> QAResponse:
        chat_prompt_params = {
            "text_chunks": get_pretty(text_chunks),
            "question": question,
            "max_sentences": self.conf["max-sentences"],
        }

        response_text = await self.get_async_llm_response(
            chat_prompt_params=chat_prompt_params
        )

        try:
            answer = json.loads(response_text)["answer"]
            answer = self.conf["unknown-answer"] if answer is None else answer
            qa_response = QAResponse(answer=answer)

            return qa_response

        except (JSONDecodeError, ValidationError):
            raise LLMResponseError(response_text=response_text)
