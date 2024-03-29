# Generated by Django 2.2.24 on 2021-11-25 10:57

import aldryn_categories.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('js_locations', '0011_auto_20210311_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='categories',
            field=aldryn_categories.fields.CategoryManyToManyField(blank=True, to='aldryn_categories.Category', verbose_name='categories'),
        ),
        migrations.AddField(
            model_name='location',
            name='contact',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Contact Name'),
        ),
        migrations.AddField(
            model_name='location',
            name='county',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='county'),
        ),
    ]
