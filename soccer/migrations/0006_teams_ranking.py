# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-29 02:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soccer', '0005_auto_20190129_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='teams',
            name='ranking',
            field=models.IntegerField(null=True),
        ),
    ]