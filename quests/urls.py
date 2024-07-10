from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ProfileView, name='ProfileView'),
    path('done/', views.QuestDoneView, name='QuestDoneView'),
    path('withdraw/', views.WithdrawView, name='WithdrawView'),
    path('<slug:slug>/', views.QuestDetail, name='QuestDetail'),
    path('token/<session_token>', views.ProfileAuth, name='ProfileAuth'),
]
