from django.db import models
import datetime
import math
import string

DEFAULT_ROW_SPACING = 40
DEFAULT_PLANT_SPACING = 25
DOUBLE_ROW_ALIASES = ["left", "right"]
TRIPLE_ROW_ALIASES = ["left", "centre", "right"]


class Field(models.Model):
    """Model representing a plot of land."""

    name = models.CharField(max_length=50)
    compass_orientation = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_bedgroups(self):
        return self.bedgroup_set.all()

    def get_beds(self):
        return Bed.objects.filter(bedgroup__field=self)

    @property
    def bedgroups(self) -> list["BedGroup"]:
        return list(self.get_bedgroups())

    @property
    def beds(self) -> list["Bed"]:
        return list(self.get_beds())

class BedGroup(models.Model):
    """
    Model representing a grouping of beds.

    Could be a polytunnel, greenhouse or a group of beds in one
    orientation.
    """

    field = models.ForeignKey("beds.Field", null=True, on_delete=models.SET_NULL)
    field_x = models.FloatField(default=0)
    field_y = models.FloatField(default=0)

    name = models.CharField(max_length=50)
    isolated = models.BooleanField(default=False)
    protected = models.BooleanField(default=False)
    field_orientation = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_beds(self):
        return self.bed_set.all()

    @property
    def beds(self):
        return self.get_beds()


class Bed(models.Model):
    """Model representing a bed planting."""

    name = models.CharField(max_length=50)
    bedgroup = models.ForeignKey("beds.BedGroup", null=True, on_delete=models.CASCADE)
    bedgroup_x = models.FloatField(default=0)
    bedgroup_y = models.FloatField(default=0)

    length = models.FloatField(help_text="Length of the bed in metres")
    width = models.FloatField(help_text="Width of the bed in metres")

    def new_planting(
        self,
        rows=3,
        row_spacing=DEFAULT_ROW_SPACING,
        plant_spacing=DEFAULT_PLANT_SPACING,
        length=None,
        width=None,
        number_plants=None,
    ):
        """Add a new planting to the bed."""

        if number_plants:
            plants_per_row = math.ceil(number_plants / rows)
            length = plants_per_row * plant_spacing

        # Default planting to full bed size
        if not length:
            length = self.length
        if not width:
            width = self.width

        new_planting = Planting(
            row_spacing=row_spacing,
            plant_spacing=plant_spacing,
            length=length,
            width=width,
        )
        new_planting.bed = self
        planting = new_planting.save()

        # Create rows
        for row in range(rows):
            new_row = planting.add_row()
            # label rows A, B, C, etc.
            new_row.label = string.ascii_uppercase[row]
            # Give the rows a Left/Center/Right alias.
            if rows == 2:
                new_row.alias = DOUBLE_ROW_ALIASES[row]
            if rows == 3:
                new_row.alias = TRIPLE_ROW_ALIASES[row]
            new_row.save()

        return planting

    def __str__(self):
        return f"{self.bedgroup}: {self.name}"


class Planting(models.Model):
    """Model representing a bed planting."""

    bed = models.ForeignKey("beds.Bed", on_delete=models.CASCADE)
    # crop = models.ForeignKey("crops.Crop", null=True, on_delete=models.SET_NULL)
    # planting_position = models.IntegerField()

    length = models.FloatField()
    width = models.FloatField()
    row_spacing = models.IntegerField()
    plant_spacing = models.IntegerField()

    # row_count = models.IntegerField()
    # plant_count = models.IntegerField()
    sown_date = models.DateField(blank=True, null=True)
    transplanted_date = models.DateField(blank=True, null=True)
    # If transplanted from another bed, record the previous planting/bed
    previous_planting = models.ForeignKey(
        "beds.Planting", null=True, on_delete=models.SET_NULL
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("accounts.CustomUser", default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop("user", None)

    def get_area(self):
        return self.length * self.width

    # def get_row_count(self):
    #     return self.row_count

    # def get_plant_count(self):
    #     return self.plant_count

    def get_row_spacing(self):
        return self.row_spacing

    def get_plant_spacing(self):
        return self.plant_spacing

    def get_length(self):
        return self.length

    def get_width(self):
        return self.width

    def get_user(self):
        return self.user

    def get_created_at(self):
        return self.created_at

    def get_updated_at(self):
        return self.updated_at

    def add_row(self, *args, **kwargs):
        """Add a row to the bed."""
        new_row = Row(**kwargs)
        new_row.bed = self
        new_row.save()
        self.save()
        return new_row

    def render_bed(self):
        """Render bed as a 2D array of row numbers."""
        bed = []
        for row in self.row_set.all():
            bed.append([0] * row.plant_count)
        return bed


class Row(models.Model):
    """Model representing a row in a bed."""

    label = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    planting = models.ForeignKey("beds.Planting", on_delete=models.CASCADE)
    plant_count = models.IntegerField()

    def new_plant(self, row_number=None):
        """Record observation of a plant in the row."""
        new_plant = Plant()
        new_plant.row = self
        new_plant.row_number = row_number
        new_plant.save()
        return new_plant

    def add_plant(self, plant=None, row_number=None):
        """Add a plant to the row, increasing row plant count."""
        if plant:
            plant.row = self
            plant.save()
        elif row_number:
            plant = self.new_plant(row_number)
        self.plant_count += 1
        self.save()


class Plant(models.Model):
    """Model representing a plant in a row. Only observed plants are represented."""

    row = models.ForeignKey("beds.row", on_delete=models.CASCADE)
    row_number = models.IntegerField()
    harvest_date = models.DateField()
    removed_date = models.DateField()

    def remove_plant(self):
        self.removed_date = datetime.date.today()
        self.save()
        self.row.plant_count -= 1
        self.row.save()
