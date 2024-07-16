import datetime

from django.utils import timezone
from telegram import Update

from tgbot.handlers.onboarding import static_text
# from tgbot.handlers.utils.info import extract_user_data_from_update
from tgbot.models import User
from tgbot.handlers.onboarding.keyboard_utils import make_keyboard_for_start_command

from telegram import ReplyKeyboardMarkup
from telegram import KeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from asgiref.sync import sync_to_async

@sync_to_async
def get_user_in_db(update, context):
    u, created = User.get_user_and_created(update, context)
    return u, created


async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    u, created = await get_user_in_db(update, context)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    await update.message.reply_text(
                                text=text,
                                parse_mode="HTML",
                                reply_markup=ReplyKeyboardMarkup(
                                                one_time_keyboard=False,
                                                resize_keyboard=True,
                                                keyboard=[
                                                    [KeyboardButton('🥷 Профиль')],
                                                    [KeyboardButton('📟 Статистика')],
                                                    [KeyboardButton('💡 Информация')],
                                                ]
                                    )
                            )

