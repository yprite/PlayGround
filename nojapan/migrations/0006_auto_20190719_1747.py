# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-19 08:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nojapan', '0005_auto_20190719_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='produce',
            field=models.ManyToManyField(blank=True, related_name='produce', to='nojapan.product'),
        ),
        migrations.AlterField(
            model_name='company',
            name='replace',
            field=models.ManyToManyField(blank=True, related_name='replace', to='nojapan.product'),
        ),
    ]
