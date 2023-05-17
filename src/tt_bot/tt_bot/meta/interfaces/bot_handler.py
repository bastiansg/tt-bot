import os

from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import BaseHandler, ContextTypes

from tt_bot.dsp import DSP
from tt_bot.logger import get_logger


logger = get_logger(__name__)


class BotHandler(ABC):
    def __init__(self, bot_name: str):
        self.dsp = DSP()
        self.bot_name = bot_name
        self.allowed_chat_ids = eval(os.getenv("ALLOWED_CHAT_IDS"))
        logger.info(f"allowed_chat_ids => {self.allowed_chat_ids}")

    @abstractmethod
    async def callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> BaseHandler:
        pass

    async def apply_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):
        # TODO is this necessary?
        if update.message is None:
            return

        chat_id = update.message.chat_id
        logger.info(f"chat_id => {chat_id}")

        if chat_id not in self.allowed_chat_ids:
            return

        await self.callback(update=update, context=context)

    @abstractmethod
    def get_handler(self) -> BaseHandler:
        pass
