from django.db import models
from django_editorjs_fields import EditorJsJSONField
from django.utils.text import slugify
from django.urls import reverse
from tgbot.models import User as Profile

class Quest(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    description =  models.CharField('Описание', max_length=200, default='')

    body_editorjs = EditorJsJSONField()

    score_need = models.IntegerField('Нужно баллов', blank=True, null=True, default=0)
    score_add = models.CharField('Дает баллов', max_length=100, default='')
    rur_add = models.CharField('Дает рублей', max_length=100, default='')

    is_major = models.BooleanField('Особенный', default=False)
    is_hide = models.BooleanField('Скрытый', default=False)

    slug = models.SlugField('Ссылка', max_length=150, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Квест"
        verbose_name_plural = "Квесты"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('QuestDetail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Quest, self).save(*args, **kwargs)

class QuestDone(models.Model):
    user = models.ForeignKey(Profile, verbose_name='ТГ-пользователь', on_delete=models.CASCADE,  blank=True, null=True)
    quest =  models.ForeignKey(Quest, verbose_name='Квест', on_delete=models.CASCADE,  blank=True, null=True)
    score = models.IntegerField('Баллы', blank=True, null=True, default=0)
    rub = models.IntegerField('Рубли', blank=True, null=True, default=0)

    class Meta:
        verbose_name = "Выполненный квест"
        verbose_name_plural = "Выполненные квесты"

    def __str__(self):
        return str(self.user.user_id)+' - '+self.quest.title

    def save(self, *args, **kwargs):
        user = Profile.objects.get(pk = self.user.pk)
        user.score_num = user.score_num + self.score
        user.quests_done_num = user.quests_done_num + 1
        user.rub_num = user.rub_num + self.rub
        user.save()
        super(QuestDone, self).save(*args, **kwargs)

class RurWithdraw(models.Model):
    user = models.ForeignKey(Profile, verbose_name='ТГ-пользователь', on_delete=models.CASCADE,  blank=True, null=True)
    rub = models.IntegerField('Рубли', blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Выплата"
        verbose_name_plural = "Выплаты"

    def __str__(self):
        return str(self.user.user_id)+' - '+str(self.rub) + ' RUR '

    def save(self, *args, **kwargs):
        user = Profile.objects.get(pk = self.user.pk)
        user.rub_num = user.rub_num - self.rub
        user.save()
        super(RurWithdraw, self).save(*args, **kwargs)
