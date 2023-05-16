from tt_bot.meta import BotHandler

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
)


class CollectiveCallHandler(BotHandler):
    def __init__(self, bot_name: str):
        super().__init__(bot_name=bot_name)

    async def callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):
        self.dsp.stop_all()
        self.dsp.start_rand_inv()

        await update.message.reply_animation(
            animation="https://media.tenor.com/lCuVmTqrAyEAAAAC/emergency-meeting-among-us.gif"  # noqa
        )

        await update.message.reply_text("https://meet.google.com/gft-kqkm-dud")
        self.dsp.stop_all()

    def get_handler(self) -> CommandHandler:
        handler = CommandHandler(
            "call",
            self.callback,
        )

        return handler
