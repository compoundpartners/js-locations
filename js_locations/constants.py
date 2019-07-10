# -*- coding: utf-8 -*-

from django.conf import settings

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
SITEMAP_PRIORITY = getattr(
    settings,
    'LOCATIONS_SITEMAP_PRIORITY',
    0.5,
)
