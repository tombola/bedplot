import svg

DEFAULT_DRAWING_SIZE = (1000, 1000)
SCALE = 20
PATH_WIDTH = 0.5


def _s(dimension):
    return dimension * SCALE


def draw_bed(bed):
    return (
        svg.Rect(
            x=_s(bed.origin_x),
            y=_s(bed.origin_y),
            width=_s(bed.width),
            height=_s(bed.length),
            fill="transparent",
            stroke="black",
        ),
    )


# # Draw bed group using svg.py
def draw_bed_group(beds):
    elements = []
    for _x, bed in enumerate(beds):
        elements += [draw_bed(bed)]

    canvas = svg.SVG(
        width=DEFAULT_DRAWING_SIZE[0],
        height=DEFAULT_DRAWING_SIZE[1],
        elements=elements,
    )
    print(canvas)
    return canvas
