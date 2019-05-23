# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-23 11:29
from __future__ import unicode_literals

import cms.models.fields
from django.db import migrations
from django.apps import apps as django_apps
import django.db.models.deletion

def forward(apps, schema_editor):
    Location = django_apps.get_model('js_locations.Location')
    from cms.models import Placeholder
    placeholder_names = ['content', 'banner', 'sidebar', 'related']

    for location in Location.objects.all():
        for placeholder_name in placeholder_names:
            placeholder_id_name = '{0}_id'.format(placeholder_name)
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
        ('js_locations', '0004_location_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='banner',
            field=cms.models.fields.PlaceholderField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location_banner', slotname='banner', to='cms.Placeholder'),
        ),
        migrations.AddField(
            model_name='location',
            name='related',
            field=cms.models.fields.PlaceholderField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location_related', slotname='related', to='cms.Placeholder'),
        ),
        migrations.AddField(
            model_name='location',
            name='sidebar',
            field=cms.models.fields.PlaceholderField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location_sidebar', slotname='sidebar', to='cms.Placeholder'),
        ),
        migrations.RunPython(forward, backwards)
    ]
