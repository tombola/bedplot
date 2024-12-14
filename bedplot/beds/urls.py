from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from bedplot.beds import views

urlpatterns = []

urlpatterns += views.PlotView.get_urls()
urlpatterns += views.BedGroupView.get_urls()
urlpatterns += views.BedView.get_urls()
