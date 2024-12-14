from django.shortcuts import render
from .models import Bed, Plot, BedGroup
from neapolitan.views import CRUDView


class PlotView(CRUDView):
    model = Plot
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
        "location",
        "length",
        "width",
    ]
