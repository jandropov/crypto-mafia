from django.contrib import admin

from . import models

#admin.site.register(models.Quest)
#admin.site.register(models.QuestDone)

@admin.register(models.Quest)
class Quest(admin.ModelAdmin):
    list_display = [
        'title',
        'score_need',
        'score_add',
        'rur_add',
    ]

@admin.register(models.QuestDone)
class QuestDone(admin.ModelAdmin):
    list_display = [
        'user', 'quest', 'score', 'rub'
    ]
    # list_filter = ["is_blocked_bot", "is_moderator"]
    # search_fields = ('username', 'user_id')

@admin.register(models.RurWithdraw)
class RurWithdraw(admin.ModelAdmin):
    list_display = [
        'user', 'rub', 'created_at'
    ]
