# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm
from aldryn_translation_tools.admin import AllTranslationsMixin

from .models import Location
from .constants import ENABLE_DX, CUSTOM_FIELDS

try:
    from js_custom_fields.forms import CustomFieldsFormMixin
except:
    class CustomFieldsFormMixin(object):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if 'custom_fields' in self.fields:
                self.fields['custom_fields'].widget = forms.HiddenInput()


class LocationAdminForm(CustomFieldsFormMixin, TranslatableModelForm):

    custom_fields = 'get_custom_fields'

    class Meta:
        model = Location
        fields = '__all__'

    def get_custom_fields(self):
        return CUSTOM_FIELDS



class LocationAdmin(AllTranslationsMixin,
                    TranslatableAdmin):
    form = LocationAdminForm
    list_display = ['__str__', 'office', 'city', 'is_published',]
    search_filter = ['translations__name', 'translations__office', 'translations__link']

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
        'custom_fields',
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
                'namespace',
                'office',
                'link',
                'is_published',
                'featured_image',
            ),
        }),
        (_('Contact (untranslated)'), {
            'fields': advanced_settings_fields,
        }),
    )

    def all_translations(self, object):
        return mark_safe(super().all_translations(object))


admin.site.register(Location, LocationAdmin)
