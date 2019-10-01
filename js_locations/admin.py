# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from parler.admin import TranslatableAdmin
from aldryn_translation_tools.admin import AllTranslationsMixin

from .models import Location
from .constants import ENABLE_DX

class LocationAdmin(AllTranslationsMixin,
                 TranslatableAdmin):
    list_display = ['__str__', 'office', 'city', 'is_published',]
    search_filter = ['translations__name', 'translations__office']

    advanced_settings_fields = (
        'phone',
        'fax',
        'email',
    )
    if ENABLE_DX:
        advanced_settings_fields += (
            'dx',
        )
    advanced_settings_fields += (
        'website',
        'address',
        'city',
        'postal_code',
        'lat',
        'lng',
        'show_on_sitemap',
        'show_on_xml_sitemap',
        'noindex',
        'nofollow',
    )

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'slug',
                'office',
                'is_published',
                'featured_image',
            ),
        }),
        (_('Contact (untranslated)'), {
            'fields': advanced_settings_fields,
        }),
    )


admin.site.register(Location, LocationAdmin)
