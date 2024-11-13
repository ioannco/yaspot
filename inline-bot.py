#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Don't forget to enable inline mode with @BotFather

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
import re
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler

from providers import init_providers, convert_ya_to_spot, MusicProviderAPI
from providers.ProviderTools import convert_spot_to_ya

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

yandex_url_regex = re.compile('.*music.yandex.ru.*')
spotify_url_regex = re.compile('.*spotify.com/track/.*')

spotify = None
yandex = None

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Hello! This is Yandex Music to Spotify url inline converter."
                                    " Usage: @ytsicbot <track_url>")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Hello! This is Yandex Music to Spotify url inline converter. "
                                    "Usage: @ytsicbot <track_url>")


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query

    if not query:  # empty query should not be handled
        return

    if yandex_url_regex.match(query):
        res = convert_ya_to_spot(query, 5)
    elif spotify_url_regex.match(query):
        res = convert_spot_to_ya(query, 5)
    else:
        provider: MusicProviderAPI
        if query.startswith("$"):
            query = query[1:]
            provider = yandex
        else:
            provider = spotify

        res = provider.search(query, 5)

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=f'{track.artists[0]} - {track.title}',
            input_message_content=InputTextMessageContent(track.url),
            thumbnail_url=track.thumbnail
        )
        for track in res
    ]

    if not results:
        return

    await update.inline_query.answer(results)


def main() -> None:
    global spotify, yandex
    credentials, yandex, spotify = init_providers()

    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(credentials["TELEGRAM_TOKEN"]).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on inline queries - show corresponding inline results
    application.add_handler(InlineQueryHandler(inline_query))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()