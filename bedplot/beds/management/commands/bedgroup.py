import djclick as click
from bedplot.beds.models import Bed, BedGroup, Field
from rich import print
from rich.table import Table
from rich.console import Console

@click.group()
def cli():
    pass

@cli.command()
@click.option("--bed-name-suffix", default="", help="Suffix to add to bed names")
@click.option("--bed-name-prefix", default="", help="Prefix to add to bed names")
@click.option("--field-orientation", "-y", default=0, help="Y position (m) w")
@click.option("--field-y", "-y", default=0, type=float, help="Y position (m) within field")
@click.option("--field-x", "-x", default=0, type=float, help="X position (m) within field")
@click.option("--field-id", "-fid", type=int, default=None, help="ID of field to add beds to")
@click.option("--path-width", "-p", default=0.5, help="Width of path between beds")
@click.option("--num-beds", "-n", default=1, help="Number of beds to create")
@click.argument("name", type=str)
@click.argument("width", type=float)
@click.argument("length", type=float)
def create(name, width, length, num_beds, path_width, field_id, field_x, field_y, field_orientation, bed_name_prefix, bed_name_suffix):
    if field_id is None:
        field_instance = Field.objects.first()
    elif isinstance(field_id, int):
        field_instance = Field.objects.get(pk=field_id)

    click.secho("Parameters:", fg='yellow')
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


@cli.command()
@click.option("--field-id", "-fid", type=int, default=None, help="ID of field list to beds for")
def list(field_id):
    if field_id is None:
        field_instance = Field.objects.first()
    elif isinstance(field_id, int):
        field_instance = Field.objects.get(pk=field_id)

    click.secho(f"BedGroups in Field '{field_instance.name}':", fg='yellow')

    bedgroups = field_instance.bedgroups

    console = Console()
    table = Table(title=f"BedGroups in Field '{field_instance.name}'")

    table.add_column("BedGroup ID", style="cyan", no_wrap=True)
    table.add_column("BedGroup Name", style="cyan", no_wrap=True)
    table.add_column("Bed Name", style="magenta")
    table.add_column("X Position", style="green")
    table.add_column("Y Position", style="green")
    table.add_column("Length", style="blue")
    table.add_column("Width", style="blue")

    for bedgroup in bedgroups:
        for bed in bedgroup.beds:
            table.add_row(
                str(bedgroup.id),
                bedgroup.name,
                bed.name,
                str(bed.bedgroup_x),
                str(bed.bedgroup_y),
                str(bed.length),
                str(bed.width),
            )

    console.print(table)


if __name__ == "__main__":
    cli()
