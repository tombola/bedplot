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


def bed_svg_view(request):
    beds = Bed.objects.all()
    context = {"svg": draw_bed_group(beds).as_str()}
    return render(request, "beds/bed_svg.html", context)
