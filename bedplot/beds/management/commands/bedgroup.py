import djclick as click
from bedplot.beds.models import Bed, BedGroup

@click.command()

@click.option("--field-orientation", "-y", default=0, help="Y position (m) w")
@click.option("--field-y", "-y", default=0, help="Y position (m) within field")
@click.option("--field-x", "-x", default=0, help="X position (m) within field")
@click.option("--field-id", "-fid", default=0, help="ID of field to add beds to")
@click.option("--path-width", "-p", default=0.5, help="Width of path between beds")
@click.option("--number-beds", "-n", default=1, help="Number of beds to create")
@click.argument("length", type=float)
@click.argument("width", type=float)
@click.argument("name", type=float)
def command(name, width, length, number_beds, path_width, field_id, field_x, field_y):
    click.secho(f"Create {number_beds} beds {path_width}m apart", fg='cyan')
    # Create beds
    bedgroup = BedGroup.objects.create(
        name=name,
        field=field_id,
        field_x=field_x,
        field_y=field_y,
    )
    for i, bed in enumerate(range(number_beds)):
        click.secho(f"Creating bed {bed}", fg='green')
        Bed.objects.create(
            name=f"Bed {bed}",
            width=width,
            length=length,
            bedgroup_x=i * (width + path_width),
            bedgroup_y=0,
        )
        pass
