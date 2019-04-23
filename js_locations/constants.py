# -*- coding: utf-8 -*-

from django.conf import settings

ENABLE_DX = getattr(
    settings,
    'LOCATIONS_ENABLE_DX',
    False,
)

