from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.NewsList, name='NewsList'),
    path('<slug:slug>/', views.NewsDetail, name='NewsDetail'),
]
