import datetime

from django.utils import timezone
from telegram import ParseMode, Update

from tgbot.models import User
from django.contrib.auth.models import User as DjangoUser

def get_stat(update: Update, context) -> None:
    u = User.get_user(update, context)

    identificator = str(u.identificator)
    score = str(u.score_num)
    rub_num = str(u.rub_num)
    quests_done_num = str(u.quests_done_num)


    update.message.reply_text("📟 Статистика:\n"+\
                              "├🎮Игрок: <b>" + identificator +'</b>'+\
                         "\n├🎲Очки: <b>" + score +'</b>'+\
                       "\n├💴Рубли: <b>" + rub_num +'</b>'+\
               "\n└✔️Квесты: <b>" + quests_done_num+'</b>',
               parse_mode="HTML")

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
