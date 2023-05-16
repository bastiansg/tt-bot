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
        self.dsp.stop_all()
        self.dsp.start_rand_inv()

        response = requests.get(self.url)
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, features="html.parser")

        # FIXME how to extract this without hardcoding?
        li_elems = soup.find_all("li")
        response = li_elems[1].get_text(separator=" ", strip=True)

        response = self.parse_response_text(response)
        await update.message.reply_animation(
            animation="https://media.tenor.com/RCBLM9AmJzkAAAAd/dollar-bills-cash.gif"  # noqa
        )

        await update.message.reply_text(response)

        self.dsp.stop_rand_inv()
        self.dsp.clear()

    def get_handler(self) -> CommandHandler:
        handler = CommandHandler(
            "blue",
            self.callback,
        )

        return handler
