# Generated by Django 5.1.4 on 2024-12-27 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beds', '0003_rename_plot_field_alter_bed_length_alter_bed_width'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bed',
            old_name='location',
            new_name='bed_group',
        ),
    ]
