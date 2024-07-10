import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('', include('landing.urls')),
    path('tghook/', include('tgbot.urls')),
    path('tgadmin/', admin.site.urls),
#     path('news/', include('news.urls')),
    path('me/', include('quests.urls')),
    path('editorjs/', include('django_editorjs_fields.urls')),
    path('sentry-debug/', trigger_error),

    #path('__debug__/', include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
