from django.contrib import admin
from django.urls import path,include

from . import views
urlpatterns = [
    path('',views.index),
    path('game/<int:id>/<str:name>/',views.game),
]