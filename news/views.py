from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

from .models import *

def NewsList(request):
    n = 274209743
    new_strn = ''
    for a in str(n):
        new_strn = new_strn + str(int(a)+1)
    print(new_strn)
    news_list = Article.objects.all().order_by('-pk')
    return render(request, 'news/newslist.html', {'news_list':news_list})

def NewsDetail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'news/news_article_detail.html', {'article':article})
