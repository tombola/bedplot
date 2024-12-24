from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from bedplot.beds import views

urlpatterns = []

urlpatterns += views.FieldView.get_urls()
urlpatterns += views.BedGroupView.get_urls()
urlpatterns += views.BedView.get_urls()

urlpatterns += [
    path("bed/plot", views.bed_svg_view, name="bed_svg_view"),
]
