# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-29 02:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('soccer', '0004_auto_20190110_1420'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchPredictVariables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x1', models.FloatField(blank=True, default=None, null=True)),
                ('x2', models.FloatField(blank=True, default=None, null=True)),
                ('x3', models.FloatField(blank=True, default=None, null=True)),
                ('x4', models.FloatField(blank=True, default=None, null=True)),
                ('x5', models.FloatField(blank=True, default=None, null=True)),
                ('x6', models.FloatField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Weigth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('w1', models.FloatField(blank=True, default=None, null=True)),
                ('w2', models.FloatField(blank=True, default=None, null=True)),
                ('w3', models.FloatField(blank=True, default=None, null=True)),
                ('w4', models.FloatField(blank=True, default=None, null=True)),
                ('w5', models.FloatField(blank=True, default=None, null=True)),
                ('w6', models.FloatField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='matchs',
            name='code',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='matchs',
            name='seq',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='matchpredictvariables',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soccer.Matchs'),
        ),
    ]
