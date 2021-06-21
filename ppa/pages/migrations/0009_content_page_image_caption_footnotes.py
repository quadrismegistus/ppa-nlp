# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-11 19:47
from __future__ import unicode_literals

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0008_contributor_page"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contentpage",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    ("paragraph", wagtail.core.blocks.RichTextBlock()),
                    (
                        "image",
                        wagtail.core.blocks.StructBlock(
                            [
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                (
                                    "caption",
                                    wagtail.core.blocks.RichTextBlock(
                                        features=["bold", "italic", "link"]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "footnotes",
                        wagtail.core.blocks.RichTextBlock(
                            classname="footnotes",
                            features=["ol", "ul", "bold", "italic", "link"],
                        ),
                    ),
                    ("document", wagtail.documents.blocks.DocumentChooserBlock()),
                ]
            ),
        ),
    ]
