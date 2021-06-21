# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-11-12 21:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0040_page_draft_title"),
        ("pages", "0002_contentpage"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="homepage",
            options={"verbose_name": "homepage"},
        ),
        migrations.AddField(
            model_name="homepage",
            name="page_preview_1",
            field=models.ForeignKey(
                blank=True,
                help_text="First page to preview on the home page as a card",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailcore.Page",
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="page_preview_2",
            field=models.ForeignKey(
                blank=True,
                help_text="Second page to preview on the home page as card",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailcore.Page",
            ),
        ),
    ]
