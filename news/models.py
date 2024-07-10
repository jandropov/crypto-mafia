from django.db import models
from django_editorjs_fields import EditorJsJSONField
from django.utils.text import slugify
from django.urls import reverse

class Article(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    description =  models.CharField('Описание' ,max_length=200)

    text = models.TextField('Тестовый текст')
    body_editorjs = EditorJsJSONField()

    slug = models.SlugField('Ссылка', max_length=150, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('NewsDetail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)
