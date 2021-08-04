# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-09 17:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("archive", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Collection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name="digitizedwork",
            name="publisher",
            field=models.TextField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="digitizedwork",
            name="collections",
            field=models.ManyToManyField(blank=True, to="archive.Collection"),
        ),
    ]
