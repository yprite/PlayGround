# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-12 04:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soccer', '0017_auto_20190712_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seasons',
            name='season',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
