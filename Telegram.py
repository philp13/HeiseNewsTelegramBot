import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
import Scraper

scraper = Scraper.Scraper()

with open('telegram_bot.txt') as f:
    token = f.read()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    today_news = scraper.get_newsticker_from_today()
    for item in today_news:
        await update.message.reply_text(item[0] + " --- " + item[1] + " --- " + item[2])


def main() -> None:
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("news", news))
    application.run_polling()


if __name__ == '__main__':
    main()
