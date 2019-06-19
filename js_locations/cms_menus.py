# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import get_language_from_request, ugettext as _

from cms.menu_bases import CMSAttachMenu
from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from .models import Location

class LocationMenu(CMSAttachMenu):
    """
    Provides an attachable menu of all locations.
    """
    name = _('JumpSuite Locations Menu')

    def get_nodes(self, request):
        nodes = []
        language = get_language_from_request(request, check_path=True)
        locations = (Location.objects.published().language(language)
                               .active_translations(language))

        for location in locations:
            try:
                url = location.get_absolute_url(language=language)
            except NoReverseMatch:
                url = None
            if url:
                node = NavigationNode(
                    location.safe_translation_getter(
                        'name', default=_('location: {0}').format(location.pk),
                        language_code=language),
                    url,
                    location.pk,
                )
                nodes.append(node)
        return nodes

menu_pool.register_menu(LocationMenu)
