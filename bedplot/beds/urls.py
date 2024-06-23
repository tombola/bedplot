from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from bedplot.beds import views

urlpatterns = [
    path('beds/', views.bed_list, name='bed_list'),
]
