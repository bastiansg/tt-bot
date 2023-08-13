import tiktoken

from typing import Any
from rich.console import Console
from abc import ABC, abstractmethod

from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from tt_bot.logger import get_logger
from tt_bot.cache import async_cache
from tt_bot.utils.yaml_data import load_yaml
from tt_bot.utils.json_data import get_pretty
from tt_bot.utils.lgchain import parse_openai_callback


console = Console()
logger = get_logger(__name__)


class OpenAIChatLLM(ABC):
    def __init__(self, conf_path: str):
        self.conf = load_yaml(conf_path)
        self.llm = ChatOpenAI(
            model_name=self.conf["model-name"],
            max_tokens=self.conf["max-tokens"],
            temperature=self.conf["temperature"],
        )

        system_message_prompt = SystemMessagePromptTemplate.from_template(
            self.conf["system-prompt-template"]
        )

        human_message_prompt = HumanMessagePromptTemplate.from_template(
            self.conf["human-prompt-template"]
        )

        self.chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        self.enc = tiktoken.encoding_for_model(self.conf["model-name"])

    @property
    def name(self):
        return self.__class__.__name__

    def get_token_len(self, text: str) -> int:
        return len(self.enc.encode(text))

    @async_cache
    async def get_async_llm_response(
        self,
        chat_prompt_params: dict,
    ) -> str:
        with console.status(f"waiting for {self.name} response..."):
            with get_openai_callback() as callback:
                messages = self.chat_prompt.format_prompt(
                    **chat_prompt_params
                ).to_messages()

                system_prompt = messages[0].content
                human_prompt = messages[1].content

                logger.debug(f"system_prompt => {system_prompt}")
                logger.debug(f"human_prompt => {human_prompt}")

                prompt_token_len = self.get_token_len(
                    system_prompt
                ) + self.get_token_len(human_prompt)

                logger.info(f"prompt_token_len => {prompt_token_len}")
                llm_response = await self.llm.apredict_messages(messages)

                openai_callback = parse_openai_callback(callback)
                logger.info(get_pretty(openai_callback))

                response_text = llm_response.content
                return response_text

    @abstractmethod
    async def async_generate(self) -> Any:
        pass
