# Generated by Django 5.1.4 on 2024-12-30 16:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beds', '0004_rename_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='bedgroup',
            name='field',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='beds.field'),
        ),
    ]
