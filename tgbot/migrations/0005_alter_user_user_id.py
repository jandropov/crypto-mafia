# Generated by Django 3.2.8 on 2024-07-18 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0004_auto_20240717_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ТГ-id'),
        ),
    ]
