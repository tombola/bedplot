from svgwrite import Drawing
from svgwrite.container import Group


DEFAULT_DRAWING_SIZE = (1000, 1000)


def draw_bed_group(beds):
    dwg = Drawing(size=DEFAULT_DRAWING_SIZE, debug=True)
    scale = 20
    path_width = 0.5
    for _x, bed in enumerate(beds):
        dwg.add(
            dwg.rect(
                insert=(_x * bed.width * scale + _x * path_width * scale, bed.origin_y),
                size=(bed.width * scale, bed.length * scale),
                fill="white",
                stroke="black",
            )
        )
    return dwg
