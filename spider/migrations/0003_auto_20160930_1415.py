# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-30 06:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spider', '0002_process'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='process',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='song',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
