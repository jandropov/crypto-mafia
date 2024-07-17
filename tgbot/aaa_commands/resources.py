import datetime

from django.utils import timezone
from telegram import Update

from tgbot.models import User
from django.contrib.auth.models import User as DjangoUser
from asgiref.sync import sync_to_async


@sync_to_async
def get_user_in_db(update, context):
    u = User.get_user(update, context)
    return u


async def get_links(update: Update, context) -> None:
    u = await get_user_in_db(update, context)

    await update.message.reply_text("💡 Информация:\n\n"\
                              "Игра призвана отсеять слабых и выделить лучших, наградить участников адреналином, весельем и хорошим настроением. "\
                              "Также в игре присутсвуют неплохие финансовые вознаграждения, благодаря которым ты можешь хорошо подзаработать.\n"\
                              "Этот бот является ключом в твой личный профиль, где ты увидишь список заданий и вознаграждений.\n"\
                              "Ознакомься с кнопками бота, заходи в профиль и начинай играть, желаю удачи!\n\n",
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

#  update.message.reply_text("💡 Информация:\n\n"\
#                               "Игра призвана отсеять слабых и выделить лучших, наградить участников адреналином, весельем и хорошим настроением. "\
#                               "Также в игре присутсвуют неплохие финансовые вознаграждения, благодаря которым ты можешь хорошо подзаработать.\n"\
#                               "Этот бот является ключом в твой личный профиль, где ты увидишь список заданий и вознаграждений.\n"\
#                               "Ознакомься с кнопками бота, заходи в профиль и начинай играть, желаю удачи!\n\n"
#                               "🔗 Актуальные ресурсы:\n"+\
#                               "├Веб-сайт: <b><a href='https://don-rave.com/'>don-rave.com</a></b>"+\
#                             "\n├Телеграмм-канал: <b>@don_rave</b>"+\
#                             "\n└Менеджер: @don_rave_mod",
#             parse_mode="HTML")