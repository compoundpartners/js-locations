# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

from . import DEFAULT_APP_NAMESPACE


class JSLocationsApp(CMSApp):
    name = _('JumpSuite Locations')
    # verbose_name = 'JumpSuite Locations'
    app_name = DEFAULT_APP_NAMESPACE
    urls = ['js_locations.urls']  # COMPAT: CMS3.2

    def get_urls(self, *args, **kwargs):
        return self.urls

apphook_pool.register(JSLocationsApp)
