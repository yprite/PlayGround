# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-19 05:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nojapan', '0003_auto_20190719_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='produce',
        ),
        migrations.AddField(
            model_name='company',
            name='produce',
            field=models.ManyToManyField(related_name='produce', to='nojapan.product'),
        ),
        migrations.RemoveField(
            model_name='company',
            name='replace',
        ),
        migrations.AddField(
            model_name='company',
            name='replace',
            field=models.ManyToManyField(related_name='replace', to='nojapan.product'),
        ),
    ]
