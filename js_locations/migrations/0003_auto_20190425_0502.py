# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-25 05:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('js_locations', '0002_location_dx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='dx',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='DX'),
        ),
    ]