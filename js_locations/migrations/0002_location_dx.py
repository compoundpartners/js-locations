# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-23 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('js_locations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='dx',
            field=models.TextField(blank=True, default='', verbose_name='DX'),
        ),
    ]