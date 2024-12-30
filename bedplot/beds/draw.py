import svg
from typing import List
from bedplot.beds.models import Field, BedGroup, Bed

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
        ),
    )


def draw_bedgroup(bedgroup: BedGroup) -> svg.G:
    elements = []
    for _x, bed in enumerate(bedgroup.beds):
        elements += [draw_bed(bed)]
    field_transform = f"translate({_s(bedgroup.field_x)}, {_s(bedgroup.field_y)})"
    return svg.G(elements=elements, transform=field_transform)


def draw_field(field: Field) -> svg.G:
    elements = []
    bedgroups = field.bedgroups
    for _x, bedgroup in enumerate(bedgroups):
        elements += [draw_bedgroup(bedgroup)]

    # compass_transform = f"rotate({field.compass_orientation})"
    return svg.G(elements=elements, transform=None)
