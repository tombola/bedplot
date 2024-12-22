from django.shortcuts import render
from .models import Bed, Plot, BedGroup
from neapolitan.views import CRUDView
from django.http import HttpResponse
import svgwrite


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


def bed_svg_view(request):
    beds = Bed.objects.all()
    dwg = svgwrite.Drawing(size=(1000, 1000))

    # TODO: separate this logic into a separate function
    scale = 20
    for _x, bed in enumerate(beds):
        dwg.add(
            dwg.rect(
                insert=(_x * scale * 1.5, bed.origin_y),
                size=(bed.width * scale, bed.length * scale),
                fill="gray",
            )
        )

    # response = HttpResponse(dwg.tostring(), content_type="image/svg+xml")
    # return response
    context = {"svg": dwg.tostring()}
    return render(request, "beds/bed_svg.html", context)
