# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from parler.admin import TranslatableAdmin
from aldryn_translation_tools.admin import AllTranslationsMixin

from .models import Location

class LocationAdmin(AllTranslationsMixin,
                 TranslatableAdmin):
    list_display = ['__str__', 'office', 'city', 'is_published',]
    search_filter = ['translations__name', 'translations__office']
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'slug',
                'office',
                'is_published',
            ),
        }),
        (_('Contact (untranslated)'), {
            'fields': (
                'phone',
                'fax',
                'email',
                'website',
                'address',
                'postal_code',
                'city',
                'lat',
                'lng'
            )
        }),
    )


admin.site.register(Location, LocationAdmin)
