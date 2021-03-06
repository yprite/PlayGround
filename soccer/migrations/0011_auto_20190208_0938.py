# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-02-08 00:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('soccer', '0010_auto_20190130_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leagues',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='leagues',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='soccer.Levels'),
        ),
        migrations.AlterField(
            model_name='leagues',
            name='nation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='soccer.Nations'),
        ),
    ]
