import djclick as click
from bedplot.beds.models import Bed, BedGroup, Field

@click.command()

@click.option("--bed-name-suffix", default="", help="Suffix to add to bed names")
@click.option("--bed-name-prefix", default="", help="Prefix to add to bed names")
@click.option("--field-orientation", "-y", default=0, help="Y position (m) w")
@click.option("--field-y", "-y", default=0, help="Y position (m) within field")
@click.option("--field-x", "-x", default=0, help="X position (m) within field")
@click.option("--field-id", "-fid", type=int, default=None, help="ID of field to add beds to")
@click.option("--path-width", "-p", default=0.5, help="Width of path between beds")
@click.option("--num-beds", "-n", default=1, help="Number of beds to create")
@click.argument("name", type=str)
@click.argument("width", type=float)
@click.argument("length", type=float)
def command(name, width, length, num_beds, path_width, field_id, field_x, field_y, field_orientation, bed_name_prefix, bed_name_suffix):
    if field_id is None:
        field_instance = Field.objects.first()
    elif isinstance(field_id, int):
        field_instance = Field.objects.get(pk=field_id)

    click.secho(f"Parameters:", fg='yellow')
    click.secho(f"  name: {name}", fg='cyan')
    click.secho(f"  width: {width}m", fg='cyan')
    click.secho(f"  length: {length}m", fg='cyan')
    click.secho(f"  --number-beds: {num_beds}", fg='yellow')
    click.secho(f"  --path-width: {path_width}", fg='yellow')
    click.secho(f"  --field-id: {field_id}", fg='yellow')
    click.secho(f"  --field-x: {field_x}", fg='yellow')
    click.secho(f"  --field-y: {field_y}", fg='yellow')
    click.secho(f"  --bed-name-prefix: {bed_name_prefix}", fg='yellow')
    click.secho(f"  --bed-name-suffix: {bed_name_suffix}", fg='yellow')
    click.echo()

    click.secho(f"Create 1 bedgroup: '{name}'", fg='cyan')
    click.secho(f"    Add {num_beds} beds {path_width}m apart:", fg='cyan')
    bed_names = []
    for bed_num in range(num_beds):
        bed_name = f"{bed_name_prefix}{bed_num + 1}{bed_name_suffix}"
        bed_names.append(bed_name)
        click.secho(f"      {bed_name}", fg='cyan')

    if not click.confirm(f"Do you want to create {num_beds} beds with the given parameters?", default=True):
        click.secho("Operation cancelled.", fg='red')
        return

    bedgroup = BedGroup.objects.create(
        name=name,
        field=field_instance,
        field_x=field_x,
        field_y=field_y,
    )
    bedgroup.save()
    click.echo()
    click.secho(f"BedGroup '{name}' created with ID: {bedgroup.id}", fg='green')

    for bed_num, bed_name in enumerate(bed_names):
        click.secho(f"  Creating bed {bed_num}", fg='green')
        bed = Bed.objects.create(
            name=bed_name,
            bedgroup=bedgroup,
            width=width,
            length=length,
            bedgroup_x=bed_num * (width + path_width),
            bedgroup_y=0,
        )
        bed.save()
        click.secho(f"    Bed '{bed.id}:{bed_name}' created.", fg='green')
