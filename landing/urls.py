from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.LandingView, name='LandingView'),
    path('rating/', views.RatingView, name='RatingView'),
    path('non-auth/', views.NAuthView, name='NAuthView'),
]
