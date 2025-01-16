from django.contrib import admin
from bedplot.beds.models import Bed, BedGroup, Field

admin.site.register(Bed)
admin.site.register(BedGroup)
admin.site.register(Field)