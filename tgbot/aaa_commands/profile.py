import datetime

from django.utils import timezone

from telegram import Update, WebAppInfo
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update


from tgbot.models import User
from django.contrib.auth.models import User as DjangoUser
from asgiref.sync import sync_to_async

@sync_to_async
def get_user_in_db(update, context):
    u = User.get_user(update, context)
    return u

@sync_to_async
def save_in_db(u):
    return u.save()


async def get_profile(update: Update, context) -> None:
    u = await get_user_in_db(update, context)

    token_gen = DjangoUser.objects.make_random_password()
    u.session_token = token_gen
    await save_in_db(u)

    keyboard = [
            [InlineKeyboardButton("🥷 Профиль", url = "https://f102-2a09-bac5-31cc-369-00-57-157.ngrok-free.app:8000/me/token/"+token_gen)],
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)


    await update.message.reply_text('🥷 Профиль:\n'+\
                            '├Cсылка на твой профиль: <b><a href="http://app.crypto-mafia.xyz:8000/me/token/'+token_gen+'">ТЫЦ!</a></b>\n'+\
                            '├Длительность сессии - <b>5 минут</b>\n'+\
                            '└Ccылка одноразовая.'+\
                            '\n\nДля повторного входа воспользуйся кнопкой.',
                            parse_mode='HTML',)

    # Создает инлайн клаву
    # update.message.reply_text(text=text,
    #                           reply_markup=make_keyboard_for_start_command())


# def secret_level(update: Update, context) -> None:
#     # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
#     """ Pressed 'secret_level_button_text' after /start command"""
#     user_id = extract_user_data_from_update(update)['user_id']
#     text = static_text.unlock_secret_room.format(
#         user_count=User.objects.count(),
#         active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
#     )
#
#     context.bot.edit_message_text(
#         text=text,
#         chat_id=user_id,
#         message_id=update.callback_query.message.message_id,
#         parse_mode=ParseMode.HTML
#     )
