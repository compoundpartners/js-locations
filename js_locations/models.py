# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from django.utils.translation import ugettext_lazy as _, override, force_text
from six import text_type

from aldryn_translation_tools.models import (
    TranslatedAutoSlugifyMixin,
    TranslationHelperMixin,
)
from cms.utils.i18n import get_current_language, get_default_language
from parler.models import TranslatableModel, TranslatedFields

from .managers import LocationManager
from . import DEFAULT_APP_NAMESPACE


@python_2_unicode_compatible
class Location(TranslationHelperMixin, TranslatedAutoSlugifyMixin,
            TranslatableModel):
    slug_source_field_name = 'name'
    translations = TranslatedFields(
        name = models.CharField(_('Display name'), max_length=255),
        slug = models.SlugField(
            _('slug'), max_length=255, default='',
            blank=True,
            help_text=_("Leave blank to auto-generate a unique slug.")),
        office = models.CharField(_('Office name'), max_length=255,
            blank=True)
    )
    address = models.TextField(
        verbose_name=_('address'), blank=True)
    postal_code = models.CharField(
        verbose_name=_('postal code'), max_length=20, blank=True)
    city = models.CharField(
        verbose_name=_('city'), max_length=255, blank=True)
    phone = models.CharField(
        verbose_name=_('phone'), null=True, blank=True, max_length=100)
    fax = models.CharField(
        verbose_name=_('fax'), null=True, blank=True, max_length=100)
    email = models.EmailField(
        verbose_name=_('email'), blank=True, default='')
    website = models.URLField(
        verbose_name=_('website'), null=True, blank=True)
    lat = models.FloatField(_('Latitude'), null=True, blank=True)
    lng = models.FloatField(_('Longitude'), null=True, blank=True)
    is_published = models.BooleanField(
        verbose_name=_('show on website'), default=True)

    objects = LocationManager()

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return self.safe_translation_getter('name')

    def get_absolute_url(self, language=None):
        if not language:
            language = get_current_language() or get_default_language()
        slug, language = self.known_translation_getter(
            'slug', None, language_code=language)
        if slug:
            kwargs = {'slug': slug}
        else:
            kwargs = {'pk': self.pk}
        with override(language):
            return reverse('%s:location-detail' % DEFAULT_APP_NAMESPACE, kwargs=kwargs)
