# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-08 20:04
from __future__ import unicode_literals

from django.db import migrations, models


def blanks_to_nulls(apps, schema_editor):
    # convert empty string to null before converting to integer
    DigitizedWork = apps.get_model("archive", "DigitizedWork")
    DigitizedWork.objects.filter(pub_date="").update(pub_date=None)


def nulls_to_blanks(apps, schema_editor):
    # convert nulls to empty string for backwards migration
    DigitizedWork = apps.get_model("archive", "DigitizedWork")
    DigitizedWork.objects.filter(pub_date__isnull=True).update(pub_date="")


class Migration(migrations.Migration):

    dependencies = [
        ("archive", "0003_add_description_collection"),
    ]

    operations = [
        # alter to allow null
        migrations.AlterField(
            model_name="digitizedwork",
            name="pub_date",
            field=models.CharField(
                max_length=255, verbose_name="Publication Date", blank=True, null=True
            ),
        ),
        # convert empty string to null
        migrations.RunPython(blanks_to_nulls, reverse_code=nulls_to_blanks),
        # convert string to integer
        migrations.AlterField(
            model_name="digitizedwork",
            name="pub_date",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Publication Date"
            ),
        ),
    ]
