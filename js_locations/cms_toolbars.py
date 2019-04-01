# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext as _, get_language_from_request
from six import iteritems

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse
from parler.models import TranslatableModel

from .models import Location
from . import DEFAULT_APP_NAMESPACE


def get_obj_from_request(model, request,
                         pk_url_kwarg='pk',
                         slug_url_kwarg='slug',
                         slug_field='slug'):
    """
    Given a model and the request, try to extract and return an object
    from an available 'pk' or 'slug', or return None.

    Note that no checking is done that the view's kwargs really are for objects
    matching the provided model (how would it?) so use only where appropriate.
    """
    language = get_language_from_request(request, check_path=True)
    kwargs = request.resolver_match.kwargs
    mgr = model.objects
    if pk_url_kwarg in kwargs:
        return mgr.filter(pk=kwargs[pk_url_kwarg]).first()
    elif slug_url_kwarg in kwargs:
        # If the model is translatable, and the given slug is a translated
        # field, then find it the Parler way.
        filter_kwargs = {slug_field: kwargs[slug_url_kwarg]}
        translated_fields = model._parler_meta.get_translated_fields()
        if (issubclass(model, TranslatableModel) and
                slug_url_kwarg in translated_fields):
            return mgr.active_translations(language, **filter_kwargs).first()
        else:
            # OK, do it the normal way.
            return mgr.filter(**filter_kwargs).first()
    else:
        return None


def get_admin_url(action, action_args=[], **url_args):
    """
    Convenience method for constructing admin-urls with GET parameters.
    """
    base_url = admin_reverse(action, args=action_args)
    # Converts [{key: value}, …] => ["key=value", …]
    url_arg_list = sorted(iteritems(url_args))
    params = ["=".join([str(k), str(v)]) for (k, v) in url_arg_list]
    if params:
        return "?".join([base_url, "&".join(params)])
    else:
        return base_url


@toolbar_pool.register
class LocationsToolbar(CMSToolbar):
    # watch_models must be a list, not a tuple
    # see https://github.com/divio/django-cms/issues/4135
    watch_models = [Location, ]
    supported_apps = ('js_locations', )

    def populate(self):
        user = getattr(self.request, 'user', None)
        try:
            view_name = self.request.resolver_match.view_name
        except AttributeError:
            view_name = None

        if user and view_name:
            language = get_language_from_request(self.request, check_path=True)
            location = None
            if view_name == '%s:location-detail' % DEFAULT_APP_NAMESPACE:
                location = get_obj_from_request(Location, self.request)
            elif view_name == '%s:location-list' % DEFAULT_APP_NAMESPACE:
                pass
            else:
                # We don't appear to be on any js_locations views so this
                # menu shouldn't even be here.
                return

            menu = self.toolbar.get_or_create_menu('locations-app', "Locations")
            change_location_perm = user.has_perm('js_locations.change_location')
            add_location_perm = user.has_perm('js_locations.add_location')
            location_perms = [change_location_perm, add_location_perm]

            if change_location_perm:
                url = admin_reverse('js_locations_location_changelist')
                menu.add_sideframe_item(_('Location list'), url=url)

            if add_location_perm:
                url_args = {}
                if language:
                    url_args.update({"language": language})
                url = get_admin_url('js_locations_location_add', **url_args)
                menu.add_modal_item(_('Add new location'), url=url)

            if change_location_perm and location:
                url = get_admin_url('js_locations_location_change', [location.pk, ])
                menu.add_modal_item(_('Edit location'), url=url, active=True)
