# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-30 07:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soccer', '0008_auto_20190130_1610'),
    ]

    operations = [
        migrations.RenameField(
            model_name='matchpredictvariables',
            old_name='x1',
            new_name='a_x1',
        ),
        migrations.RenameField(
            model_name='matchpredictvariables',
            old_name='x2',
            new_name='a_x2',
        ),
        migrations.RenameField(
            model_name='matchpredictvariables',
            old_name='x3',
            new_name='a_x3',
        ),
        migrations.RenameField(
            model_name='matchpredictvariables',
            old_name='x4',
            new_name='a_x4',
        ),
        migrations.RenameField(
            model_name='matchpredictvariables',
            old_name='x5',
            new_name='a_x5',
        ),
        migrations.RenameField(
            model_name='matchpredictvariables',
            old_name='x6',
            new_name='a_x6',
        ),
        migrations.AddField(
            model_name='matchpredictvariables',
            name='h_x1',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='matchpredictvariables',
            name='h_x2',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='matchpredictvariables',
            name='h_x3',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='matchpredictvariables',
            name='h_x4',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='matchpredictvariables',
            name='h_x5',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='matchpredictvariables',
            name='h_x6',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
