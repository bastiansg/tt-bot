import os

from tt_bot.logger import get_logger
from telegram.ext import ApplicationBuilder
from .handlers import (
    QAHandler,
    CollectiveCallHandler,
    BlueDollarHandler,
    PublicIP,
)


logger = get_logger(__name__)


handlers = [
    QAHandler,
    CollectiveCallHandler,
    BlueDollarHandler,
    PublicIP,
]

bot_name = os.getenv("BOT_NAME")
app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_API_KEY")).build()
for handler in handlers:
    app.add_handler(handler(bot_name=bot_name).get_handler())

app.run_polling()
