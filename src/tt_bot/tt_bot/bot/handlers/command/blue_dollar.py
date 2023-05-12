import requests

from bs4 import BeautifulSoup
from tt_bot.meta import BotHandler

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
)


class BlueDollarHandler(BotHandler):
    def __init__(self, bot_name: str):
        super().__init__(bot_name=bot_name)
        self.url = "https://www.dolarito.ar"

    def parse_response_text(self, text: str) -> str:
        text = text.replace("$ ", "$")
        text = text.replace(" Compra", "\nCompra:")
        text = text.replace("Venta", "Venta:")

        return text

    async def callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):
        response = requests.get(self.url)
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, features="html.parser")
        found_div = soup.find("div", attrs={"class": "css-c9onyv"})

        response = found_div.get_text(separator=" ", strip=True)
        response = self.parse_response_text(response)
        await update.message.reply_animation(
            animation="https://media.tenor.com/RCBLM9AmJzkAAAAd/dollar-bills-cash.gif"  # noqa
        )

        await update.message.reply_text(response)

    def get_handler(self) -> CommandHandler:
        handler = CommandHandler(
            "blue",
            self.callback,
        )

        return handler
