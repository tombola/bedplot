import svg
from typing import List
from bedplot.beds.models import Field, BedGroup, Bed
from django.urls import reverse

DEFAULT_DRAWING_SIZE = (1000, 1000)
SCALE = 20
PATH_WIDTH = 0.5


def _s(dimension):
    return dimension * SCALE


def draw_canvas(elements):
    canvas = svg.SVG(
        width=DEFAULT_DRAWING_SIZE[0],
        height=DEFAULT_DRAWING_SIZE[1],
        elements=elements,
    )
    print(canvas)
    return canvas


def draw_bed(bed: Bed) -> svg.Rect:
    return (
        svg.Rect(
            x=_s(bed.bedgroup_x),
            y=_s(bed.bedgroup_y),
            width=_s(bed.width),
            height=_s(bed.length),
            fill="transparent",
            stroke="black",
            class_="bed",
            data={'bid': bed.id},
            attributes={'hx-get': reverse('bed-detail', args=[bed.id]), "hx-target": "#sidebar", "hx-swap": "innerHTML"},
        ),
    )



def draw_bedgroup(bedgroup: BedGroup) -> svg.G:
    elements = []
    for _x, bed in enumerate(bedgroup.beds):
        elements += [draw_bed(bed)]
    elements += [svg.Text(text=bedgroup.name, x=10, y=20, class_='bedgroup-label')]
    field_transform = f"translate({_s(bedgroup.field_x)}, {_s(bedgroup.field_y)})"
    return svg.G(elements=elements, transform=field_transform, class_="bedgroup")


def draw_field(field: Field) -> svg.G:
    elements = [draw_compass(field.compass_orientation)]
    bedgroups = field.bedgroups
    for _x, bedgroup in enumerate(bedgroups):
        elements += [draw_bedgroup(bedgroup)]

    # compass_transform = f"rotate({field.compass_orientation})"
    return svg.G(elements=elements, transform=None)


def draw_compass(degrees):
    return svg.G(elements=[
        svg.Circle(cx=0, cy=0, r=50, fill="transparent", stroke="black", class_="compass",  elements=[]),
        svg.Text(text="N", x=-6, y=-30, class_="compass"),
        svg.Line(x1=0, y1=0, x2=0, y2=-50, stroke="red")
    ], transform=f"translate(650, 51) rotate({-degrees})", class_="compass")