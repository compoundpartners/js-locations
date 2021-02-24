# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.text import slugify

ENABLE_DX = getattr(
    settings,
    'LOCATIONS_ENABLE_DX',
    False,
)

SITEMAP_CHANGEFREQ = getattr(
    settings,
    'LOCATIONS_SITEMAP_CHANGEFREQ',
    'monthly',
)

CUSTOM_FIELDS = getattr(
    settings,
    'LOCATIONS_CUSTOM_FIELDS',
    {},
)

SITEMAP_PRIORITY = getattr(
    settings,
    'LOCATIONS_SITEMAP_PRIORITY',
    0.5,
)

SPECIFIC_LOCATIONS_LAYOUTS = getattr(
    settings,
    'LOCATIONS_SPECIFIC_LOCATIONS_LAYOUTS',
    (),
)
SPECIFIC_LOCATIONS_LAYOUTS = zip(list(map(lambda s: slugify(s).replace('-', '_'), ('',) + SPECIFIC_LOCATIONS_LAYOUTS)), ('default',) + SPECIFIC_LOCATIONS_LAYOUTS)

