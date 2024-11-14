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
from typing import Union
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler

from providers import init_providers, convert_ya_to_spot, SpotifyProvider, YandexMusicProvider
from providers.ProviderTools import convert_spot_to_ya
from settings import SETTINGS

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

yandex_url_regex = re.compile('.*music.yandex.ru.*')
spotify_url_regex = re.compile('.*spotify.com/track/.*')

spotify: SpotifyProvider
yandex: YandexMusicProvider

counter: int = 0

bot_description = ("This is Spotify inline search bot!\n\n"
                   f"You can search for any track in spotify just by typing \n{SETTINGS.BOT_TAG} <track name>.\n\n"
                   f"If you want to search for a track in yandex music, just add $ before the track name.\n\n"
                   f"This bot can also handle URL conversions. Just add url after the {SETTINGS.BOT_TAG} and the bot will "
                   f"convert yandex url to spotify url and vice versa!")

def choose_provider_for_query(query: str) -> tuple[str, Union[SpotifyProvider, YandexMusicProvider]]:
    if query.startswith("$"):
        query = query[1:]
        return query, yandex
    else:
        return query, spotify

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(bot_description)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(bot_description)


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query

    global counter
    print("counter", counter)
    counter += 1

    if not query:  # empty query should not be handled
        return

    if yandex_url_regex.match(query):
        res = convert_ya_to_spot(query, 5)
    elif spotify_url_regex.match(query):
        res = convert_spot_to_ya(query, 5)
    else:
        query, provider = choose_provider_for_query(query)
        res = provider.search(query, 5)

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=f'[{track.provider}] {", ".join(track.artists)} - {track.title}',
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
    yandex, spotify = init_providers()

    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(SETTINGS.TELEGRAM_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on inline queries - show corresponding inline results
    application.add_handler(InlineQueryHandler(inline_query))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()