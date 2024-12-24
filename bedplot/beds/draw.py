import svg

DEFAULT_DRAWING_SIZE = (1000, 1000)
SCALE = 20
PATH_WIDTH = 0.5


# # Draw bed group using svg.py
def draw_bed_group(beds):
    elements = []
    for _x, bed in enumerate(beds):
        elements += [
            svg.Rect(
                x=_x * bed.width * SCALE + _x * PATH_WIDTH * SCALE,
                y=bed.origin_y,
                width=bed.width * SCALE,
                height=bed.length * SCALE,
                fill="transparent",
                stroke="black",
            ),
        ]

    canvas = svg.SVG(
        width=DEFAULT_DRAWING_SIZE[0],
        height=DEFAULT_DRAWING_SIZE[1],
        elements=elements,
    )
    print(canvas)
    return canvas
