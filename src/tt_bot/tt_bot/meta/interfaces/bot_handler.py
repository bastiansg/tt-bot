from abc import abstractmethod
from telegram.ext import BaseHandler


class BotHandler:
    def __init__(self, bot_name: str):
        self.bot_name = bot_name

    @abstractmethod
    def get_handler(self) -> BaseHandler:
        raise NotImplementedError
