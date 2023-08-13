import requests

from tt_bot.meta import BotHandler
from tt_bot.logger import get_logger

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
)


logger = get_logger(__name__)


class PublicIPHandler(BotHandler):
    def __init__(self, bot_name: str):
        super().__init__(bot_name=bot_name)

    async def callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):
        self.dsp.stop_all()
        self.dsp.start_rand_inv()

        response = requests.get("https://ifconfig.me")
        status_code = response.status_code
        if status_code != 200:
            logger.error(f"status_code => {status_code}")
            await update.message.reply_text(
                f":skill ERROR: status_code {status_code}"
            )

            self.dsp.stop_all()
            return

        public_ip = response.content.decode()
        await update.message.reply_text(
            f"Office public ip: `{public_ip}`",
            parse_mode="MarkdownV2",
        )

        self.dsp.stop_all()

    def get_handler(self) -> CommandHandler:
        handler = CommandHandler(
            "ip",
            self.apply_callback,
        )

        return handler
