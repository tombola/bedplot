from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from bedplot.beds import views

urlpatterns = []

urlpatterns += views.FieldView.get_urls()
urlpatterns += views.BedGroupView.get_urls()
urlpatterns += views.BedView.get_urls()

urlpatterns += [
    path("field/draw/<int:field_id>/", views.field_svg_view, name="field_svg_view"),
    path("field/draw/", views.field_svg_view, name="field_svg_view"),
]
