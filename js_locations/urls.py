# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    LocationDetailView,
    LocationListView,
)

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$',
        LocationDetailView.as_view(), name='location-detail'),
    url(r'^(?P<slug>[A-Za-z0-9_\-]+)/$',
        LocationDetailView.as_view(), name='location-detail'),
    url(r'^$',
        LocationListView.as_view(), name='location-list'),
]
