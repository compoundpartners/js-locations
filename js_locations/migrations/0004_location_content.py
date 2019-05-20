# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-20 06:10
from __future__ import unicode_literals

import cms.models.fields
from django.db import migrations
from django.apps import apps as django_apps
import django.db.models.deletion


def forward(apps, schema_editor):
    Location = django_apps.get_model('js_locations.Location')
    from cms.models import Placeholder
    placeholder_name = 'content'
    placeholder_id_name = '{0}_id'.format(placeholder_name)

    for location in Location.objects.all():
        placeholder_id = getattr(location, placeholder_id_name, None)
        if placeholder_id is not None:
            continue
        placeholder_new = Placeholder.objects.create(slot=placeholder_name)
        setattr(location, placeholder_id_name, placeholder_new.pk)
        location.save()
    pass

def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0020_old_tree_cleanup'),
        ('js_locations', '0003_auto_20190425_0502'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='content',
            field=cms.models.fields.PlaceholderField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location_content', slotname='content', to='cms.Placeholder'),
        ),
        migrations.RunPython(forward, backwards)
    ]
