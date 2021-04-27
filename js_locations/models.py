# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    from django.core.urlresolvers import reverse, NoReverseMatch
except ImportError:
    # Django 2.0
    from django.urls import reverse, NoReverseMatch
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _, override, ugettext
from six import text_type

from aldryn_translation_tools.models import (
    TranslatedAutoSlugifyMixin,
    TranslationHelperMixin,
)
from cms.utils.i18n import get_current_language, get_default_language
from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin
from parler.models import TranslatableModel, TranslatedFields
from filer.fields.image import FilerImageField
from sortedm2m.fields import SortedManyToManyField

from .managers import LocationManager
from . import DEFAULT_APP_NAMESPACE

try:
    from custom.js_locations.models import CustomLocationMixin
except ImportError:
    class CustomLocationMixin(object):
        pass

@python_2_unicode_compatible
class Location(CustomLocationMixin,
               TranslationHelperMixin,
               TranslatedAutoSlugifyMixin,
               TranslatableModel):

    slug_source_field_name = 'name'

    translations = TranslatedFields(
        name = models.CharField(_('Display name'), max_length=255),
        slug = models.SlugField(
            _('slug'), max_length=255, default='',
            blank=True,
            help_text=_("Leave blank to auto-generate a unique slug.")),
        office = models.CharField(_('Office name'), max_length=255,
            blank=True),
        link = models.CharField(_('Link'), max_length=255,
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
    dx = models.CharField(
        verbose_name=_('DX'), max_length=255, blank=True, default='')
    content = PlaceholderField('content', related_name='location_content')
    banner = PlaceholderField('banner', related_name='location_banner')
    sidebar = PlaceholderField('sidebar', related_name='location_sidebar')
    related = PlaceholderField('related', related_name='location_related')
    featured_image = FilerImageField(
        verbose_name=_('featured image'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    show_on_sitemap = models.BooleanField(_('Show on sitemap'), null=False, default=True)
    show_on_xml_sitemap = models.BooleanField(_('Show on xml sitemap'), null=False, default=True)
    noindex = models.BooleanField(_('noindex'), null=False, default=False)
    nofollow = models.BooleanField(_('nofollow'), null=False, default=False)
    custom_fields = JSONField(blank=True, null=True)

    #app config fields and methods
    type = models.CharField(
        _('Type'),
        max_length=100,
        default='js_locations.Location',
    )
    namespace = models.CharField(
        _('Instance namespace'),
        #default=None,
        max_length=100,
        unique=True,
        blank=True,
        null=True,
    )

    cmsapp = None

    def save(self, *args, **kwargs):
        self.type = '%s.%s' % (
            self.__class__.__module__, self.__class__.__name__)
        if not self.namespace:
            self.namespace = self.safe_translation_getter('slug')
        super().save(*args, **kwargs)

    objects = LocationManager()

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        #unique_together = ('type', 'namespace')

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


@python_2_unicode_compatible
class SpecificLocationsPlugin(CMSPlugin):
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin, on_delete=models.CASCADE, related_name='+', parent_link=True)
    title = models.CharField(max_length=255, blank=True, verbose_name=_('Title'))
    layout = models.CharField(max_length=30, verbose_name=_('layout'), blank=True, null=True)
    locations = SortedManyToManyField(Location, verbose_name=_('locations'), blank=True, symmetrical=False)
    more_button_is_shown = models.BooleanField(blank=True, default=False, verbose_name=_('Show “See More Button”'))
    more_button_text = models.CharField(max_length=255, blank=True, verbose_name=_('See More Button Text'))
    more_button_link = models.CharField(max_length=255, blank=True, verbose_name=_('See More Button Link'))

    def copy_relations(self, oldinstance):
        self.locations.set(oldinstance.locations.all())

    def __str__(self):
        return self.title or ugettext('Specific locations')
