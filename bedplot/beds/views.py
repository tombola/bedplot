from django.shortcuts import render
from .models import Bed
from neapolitan.views import CRUDView


class BedView(CRUDView):
    model = Bed
    fields = [
        "name",
        "location",
        "length",
        "width",
    ]
