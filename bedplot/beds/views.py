from django.shortcuts import render
from .models import Bed, Field, BedGroup
from neapolitan.views import CRUDView
from django.http import HttpResponse
from bedplot.beds.draw import draw_bedgroup, draw_field, draw_canvas


class FieldView(CRUDView):
    model = Field
    fields = [
        "name",
        "compass_orientation",
    ]


class BedGroupView(CRUDView):
    model = BedGroup
    fields = [
        "field",
        "field_x",
        "field_y",
        "name",
        "isolated",
        "protected",
        "field_orientation",
    ]


class BedView(CRUDView):
    model = Bed
    fields = [
        "name",
        "bedgroup",
        "length",
        "width",
    ]


def field_svg_view(request, field_id):
    field = Field.objects.get(pk=field_id)
    context = {"svg": draw_canvas([draw_field(field)]).as_str()}

    return render(request, "beds/bed_svg.html", context)
