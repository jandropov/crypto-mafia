# """
#     Telegram event handlers
# """
import sys
import logging
from typing import Dict
#
# import telegram.error
# from telegram import Bot, Update, BotCommand
# from telegram.ext import (
#     Updater, Dispatcher, Filters,
#     CommandHandler, MessageHandler,
#     CallbackQueryHandler,
# )
#
# from dtb.celery import app  # event processing in async mode
from dtb.settings import TELEGRAM_TOKEN, DEBUG
#
# from tgbot.handlers.utils import files, error
# from tgbot.handlers.admin import handlers as admin_handlers
# #from tgbot.handlers.location import handlers as location_handlers
from tgbot.handlers.onboarding import handlers as onboarding_handlers
# from tgbot.handlers.broadcast_message import handlers as broadcast_handlers
# from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON
# from tgbot.handlers.broadcast_message.manage_data import CONFIRM_DECLINE_BROADCAST
# from tgbot.handlers.broadcast_message.static_text import broadcast_command
# #
# from tgbot.aaa_commands import profile
# from tgbot.aaa_commands import statistics
# from tgbot.aaa_commands import resources
#
#
# def setup_dispatcher(dp):
#     # onboarding
#     dp.add_handler(CommandHandler("start", onboarding_handlers.command_start))
#
#     # profile
#     dp.add_handler(CommandHandler("profile", profile.get_profile))
#     dp.add_handler(MessageHandler(Filters.regex('🥷 Профиль'), profile.get_profile))
#
#     # stat
#     dp.add_handler(CommandHandler("stats", statistics.get_stat))
#     dp.add_handler(MessageHandler(Filters.regex('📟 Статистика'), statistics.get_stat))
#
#     # resources
#     dp.add_handler(CommandHandler("links", resources.get_links))
#     dp.add_handler(MessageHandler(Filters.regex('💡 Информация'), resources.get_links))
#
#     # admin commands
#     # dp.add_handler(CommandHandler("admin", admin_handlers.admin))
#     # dp.add_handler(CommandHandler("stats", admin_handlers.stats))
#     # dp.add_handler(CommandHandler('export_users', admin_handlers.export_users))
#
#     # location
#     # dp.add_handler(CommandHandler("ask_location", location_handlers.ask_for_location))
#     # dp.add_handler(MessageHandler(Filters.location, location_handlers.location_handler))
#
#     # secret level
#     #dp.add_handler(CallbackQueryHandler(onboarding_handlers.secret_level, pattern=f"^{SECRET_LEVEL_BUTTON}"))
#
#     # broadcast message
#     # dp.add_handler(
#     #     MessageHandler(Filters.regex(rf'^{broadcast_command}(/s)?.*'), broadcast_handlers.broadcast_command_with_message)
#     # )
#     # dp.add_handler(
#     #     CallbackQueryHandler(broadcast_handlers.broadcast_decision_handler, pattern=f"^{CONFIRM_DECLINE_BROADCAST}")
#     # )
#
#     # files
#     # dp.add_handler(MessageHandler(
#     #     Filters.animation, files.show_file_id,
#     # ))
#
#     # handling errors
#     #dp.add_error_handler(error.send_stacktrace_to_tg_chat)
#
#     # EXAMPLES FOR HANDLERS
#     # dp.add_handler(MessageHandler(Filters.text, <function_handler>))
#     # dp.add_handler(MessageHandler(
#     #     Filters.document, <function_handler>,
#     # ))
#     # dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
#     # dp.add_handler(MessageHandler(
#     #     Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
#     #     # & Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
#     #     <function_handler>,
#     # ))
#
#     return dp
#
#
# def run_pooling():
#     """ Run bot in pooling mode """
#     updater = Updater(TELEGRAM_TOKEN, use_context=True)
#
#     dp = updater.dispatcher
#     dp = setup_dispatcher(dp)
#
#     bot_info = Bot(TELEGRAM_TOKEN).get_me()
#     bot_link = f"https://t.me/" + bot_info["username"]
#
#     print(f"Pooling of '{bot_link}' started")
#     # it is really useful to send '👋' emoji to developer
#     # when you run local test
#     #bot.send_message(text='👋', chat_id='274206743')
#     set_up_commands(bot)
#
#     updater.start_polling()
#     updater.idle()

#
# # Global variable - best way I found to init Telegram bot
# bot = Bot(TELEGRAM_TOKEN)
# try:
#     TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
# except telegram.error.Unauthorized:
#     logging.error(f"Invalid TELEGRAM_TOKEN.")
#     sys.exit(1)
#
#
# @app.task(ignore_result=True)
# def process_telegram_event(update_json):
#     update = Update.de_json(update_json, bot)
#     dispatcher.process_update(update)

#
# def set_up_commands(bot_instance: Bot) -> None:
#     langs_with_commands: Dict[str, Dict[str, str]] = {
#         'en': {
#             'profile': '🥷 Профиль',
#             'stats': '📟 Статистика',
#             'links': '💡 Информация',
#         },
#         'ru': {
#             'profile': '🥷 Профиль',
#             'stats': '📟 Статистика',
#             'links': '💡 Информация',
#         }
#     }
#
#     bot_instance.delete_my_commands()
#     for language_code in langs_with_commands:
#         bot_instance.set_my_commands(
#             language_code=language_code,
#             commands=[
#                 BotCommand(command, description) for command, description in langs_with_commands[language_code].items()
#             ]
#         )
#
#
# # WARNING: it's better to comment the line below in DEBUG mode.
# # Likely, you'll get a flood limit control error, when restarting bot too often
# #set_up_commands(bot)
#
#
# n_workers = 1 if DEBUG else 4
# dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))


#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple example of a Telegram WebApp which displays a color picker.
The static website for this website is hosted by the PTB team for your convenience.
Currently only showcases starting the WebApp via a KeyboardButton, as all other methods would
require a bot token.
"""
import json
import logging

from dtb.celery import app
from telegram import Bot

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from tgbot.aaa_commands import profile

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)




# Define a `/start` command handler.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    await update.message.reply_text(
        "Please press the button below to choose a color via the WebApp.",
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="Open the color picker!",
                web_app=WebAppInfo(url="https://python-telegram-bot.org/static/webappbot"),
            )
        ),
    )

# Handle incoming WebAppData
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Print the received data and remove the button."""
    # Here we use `json.loads`, since the WebApp sends the data JSON serialized string
    # (see webappbot.html)
    data = json.loads(update.effective_message.web_app_data.data)
    await update.message.reply_html(
        text=(
            f"You selected the color with the HEX value <code>{data['hex']}</code>. The "
            f"corresponding RGB value is <code>{tuple(data['rgb'].values())}</code>."
        ),
        reply_markup=ReplyKeyboardRemove(),
    )

bot = Bot(TELEGRAM_TOKEN)

@app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = Update.de_json(update_json, bot)
    dispatcher.process_update(update)


def run_pooling():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

   # application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("start", onboarding_handlers.command_start))
    application.add_handler(MessageHandler(filters.Regex('🥷 Профиль'), profile.get_profile))

#     application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))


    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


# if __name__ == "__main__":
#     main()