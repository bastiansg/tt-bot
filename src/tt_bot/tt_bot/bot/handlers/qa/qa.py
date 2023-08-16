from more_itertools import flatten

from tt_bot.meta import BotHandler
from tt_bot.logger import get_logger
from tt_bot.retrievals import WebRetrieval
from tt_bot.search_engines import GoogleSearchEngine
from tt_bot.text_encoders import OpenAIEncoder
from tt_bot.llm_components import LgChainQA
from tt_bot.web_extractors import (
    HTMLExtractor,
    WikiExtractor,
    LinkedinExtractor,
)

from telegram import Update
from telegram.ext import (
    MessageHandler,
    ContextTypes,
    filters,
)


logger = get_logger(__name__)


class QAHandler(BotHandler):
    def __init__(self, bot_name: str, unknown_answer: str = "I don't know"):
        super().__init__(bot_name=bot_name)
        self.unknown_answer = unknown_answer

        search_engine = GoogleSearchEngine()
        text_encoder = OpenAIEncoder()
        extractors = {
            "html": HTMLExtractor(),
            "wikipedia": WikiExtractor(),
            "linkedin": LinkedinExtractor(),
        }

        self.web_retrieval = WebRetrieval(
            search_engine=search_engine,
            text_encoder=text_encoder,
            extractors=extractors,
        )

        self.openai_qa = LgChainQA()

    def parse_query_text(self, text: str, bot_name: str) -> str:
        text = text.replace(bot_name, "")
        text = " ".join(text.split())
        text = text.strip()

        return text

    def get_reference_text(self, reference: list[dict]) -> str:
        reference_text = "\n\n".join(
            "\n".join(f"{k}: {v}" for k, v in ref.items()) for ref in reference
        )

        return reference_text

    async def callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):
        mentions = update.effective_message.parse_entities(["mention"])
        mentions = set(mentions.values())
        logger.info(f"mentions => {mentions}")

        if self.bot_name not in mentions:
            return

        message = update.message
        self.dsp.stop_all()
        self.dsp.start_rand_inv()

        query_text = self.parse_query_text(message.text, self.bot_name)
        if not query_text:
            logger.warning("No query text")
            return

        logger.info(f"query_text => {query_text}")
        retrieval_responses = await self.web_retrieval.retrieve(
            query_text=query_text
        )

        if not retrieval_responses:
            await message.reply_text(self.unknown_answer)
            return

        text_chunks = (rr.texts for rr in retrieval_responses)
        text_chunks = list(flatten(text_chunks))

        self.dsp.stop_rand_inv()
        self.dsp.start_intermittent()

        qa_answer = await self.openai_qa.async_generate(
            text_chunks, query_text
        )

        answer_text = qa_answer.answer
        if not answer_text:
            await message.reply_text(self.unknown_answer)
            return

        reference = [
            {
                "source": rr.source,
                "similarity": rr.similarity,
                "relevance": rr.relevance,
            }
            for rr in retrieval_responses
        ]

        reference_text = self.get_reference_text(reference)
        await update.message.reply_text(
            f"{answer_text}\n\n{reference_text}",
            disable_web_page_preview=True,
        )

        self.dsp.stop_all()

    def get_handler(self) -> MessageHandler:
        handler = MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.apply_callback,
        )

        return handler
