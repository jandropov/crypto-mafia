from __future__ import annotations

from typing import Union, Optional, Tuple, Dict

from django.db import models
from django.db.models import QuerySet
from telegram import Update

from dtb.settings import DEBUG
from tgbot.handlers.utils.info import extract_user_data_from_update
from utils.models import CreateUpdateTracker, nb, CreateTracker

from django.contrib.auth.models import User as DjangoUser



class User(CreateUpdateTracker):
    user_id = models.BigIntegerField('ТГ-id', primary_key=True)  # telegram_id
    username = models.CharField('ТГ-username', max_length=32, **nb)
    first_name = models.CharField('ТГ-first_name', max_length=256)
    last_name = models.CharField('ТГ-last_name', max_length=256, **nb)
    language_code = models.CharField(max_length=8, help_text="Telegram client's lang", **nb)
    deep_link = models.CharField(max_length=64, **nb)

    is_blocked_bot = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    identificator = models.BigIntegerField('Идентификатор', blank=True, null=True, default=None)

    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    is_fake = models.BooleanField(default=False)

    django_user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE,  blank=True, null=True)
    session_token = models.CharField(max_length=100, blank=True, null=True)
    score_num = models.IntegerField('Баллы', blank=True, null=True, default=0)
    rub_num = models.IntegerField('Рубли', blank=True, null=True, default=0)
    quests_done_num = models.IntegerField('Квесты', blank=True, null=True, default=0)

    class Meta:
        verbose_name = "ТГ-пользователь"
        verbose_name_plural = "ТГ-пользователи"

    def __str__(self):
        return f'@{self.username}' if self.username is not None else f'{self.identificator}'

    @classmethod
    def get_user_and_created(cls, update: Update, context) -> Tuple[User, bool]:
        """ python-telegram-bot's Update, Context --> User instance """
        data = extract_user_data_from_update(update)

        u, created = cls.objects.update_or_create(user_id=data["user_id"], defaults=data)
        if created:
            #create identificator
            new_strn = ''
            for a in str(data["user_id"]):
                new_strn = new_strn + str(int(a)+1)
            u.identificator = int(new_strn)

            # create django user
            djuser = DjangoUser.objects.create_user(u.identificator,'',str(u.identificator))
            u.django_user = djuser
            u.save()

            # Save deep_link to User model
            if context is not None and context.args is not None and len(context.args) > 0:
                payload = context.args[0]
                if str(payload).strip() != str(data["user_id"]).strip():  # you can't invite yourself
                    u.deep_link = payload
                    u.save()

        return u, created

    @classmethod
    def get_user(cls, update: Update, context) -> User:
        u, _ = cls.get_user_and_created(update, context)
        return u

    @classmethod
    def get_user_by_username_or_user_id(cls, username_or_user_id: Union[str, int]) -> Optional[User]:
        """ Search user in DB, return User or None if not found """
        username = str(username_or_user_id).replace("@", "").strip().lower()
        if username.isdigit():  # user_id
            return cls.objects.filter(user_id=int(username)).first()
        return cls.objects.filter(username__iexact=username).first()

    @property
    def invited_users(self) -> QuerySet[User]:
        return User.objects.filter(deep_link=str(self.user_id), created_at__gt=self.created_at)

    @property
    def tg_str(self) -> str:
        if self.username:
            return f'@{self.username}'
        return f"{self.first_name} {self.last_name}" if self.last_name else f"{self.first_name}"


#
# class Location(CreateTracker):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     latitude = models.FloatField()
#     longitude = models.FloatField()
#
#     def __str__(self):
#         return f"user: {self.user}, created at {self.created_at.strftime('(%H:%M, %d %B %Y)')}"
#
#     def save(self, *args, **kwargs):
#         super(Location, self).save(*args, **kwargs)
#         # Parse location with arcgis
#         from arcgis.tasks import save_data_from_arcgis
#         if DEBUG:
#             save_data_from_arcgis(latitude=self.latitude, longitude=self.longitude, location_id=self.pk)
#         else:
#             save_data_from_arcgis.delay(latitude=self.latitude, longitude=self.longitude, location_id=self.pk)
