import os

from tt_bot.qa import DocQA
from tt_bot.logger import get_logger
from tt_bot.retrieval import Retrieval

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)


from utils import remove_bot_mention, get_ref_text


logger = get_logger(__name__)
BOT_NAME = os.getenv("BOT_NAME")


doc_qa = DocQA()
retrieval = Retrieval()


async def q(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mentions = update.effective_message.parse_entities(["mention"])
    mentions = set(mentions.values())
    logger.info(f"mentions => {mentions}")

    if BOT_NAME in mentions:
        query_text = remove_bot_mention(update.message.text, BOT_NAME)
        logger.info(f"query_text => {query_text}")

        sim_chunks = await retrieval.retrieve(query_text)
        if not sim_chunks:
            await update.message.reply_text("I don't know")
            return

        response = doc_qa.get_answer(
            sim_chunks=sim_chunks,
            query_text=query_text,
        )

        ref_text = get_ref_text(response["ref"])
        await update.message.reply_text(
            f"{response['answer']}\n\n{ref_text}",
            disable_web_page_preview=True,
        )


app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_API_KEY")).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, q))
app.run_polling()
