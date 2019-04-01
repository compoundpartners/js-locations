# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext_lazy as _

from cms.wizards.wizard_pool import wizard_pool
from cms.wizards.wizard_base import Wizard
from cms.wizards.forms import BaseFormMixin

from parler.forms import TranslatableModelForm

from .models import Location
from . import DEFAULT_APP_NAMESPACE


def has_published_apphook():
    """
    Returns a list of app_configs that are attached to a published page.
    """
    try:
        reverse('%s:location-list' % DEFAULT_APP_NAMESPACE)
        return True
    except NoReverseMatch:
        pass
    return False


class LocationWizard(Wizard):

    def get_success_url(self, **kwargs):
        if has_published_apphook():
            return super(LocationWizard, self).get_success_url(**kwargs)
        else:
            return None

    def user_has_add_permission(self, user, **kwargs):
        """
        Return True if the current user has permission to add a location.
        :param user: The current user
        :param kwargs: Ignored here
        :return: True if user has add permission, else False
        """
        if user.is_superuser or user.has_perm("js_locations.add_location"):
            return True
        return False


class CreateLocationForm(BaseFormMixin, TranslatableModelForm):
    class Meta:
        model = Location
        fields = ['name', 'office', 'address', 'postal_code', 'city',
                  'phone', 'email', 'website']


location_wizard = LocationWizard(
    title=_('New location'),
    weight=300,
    form=CreateLocationForm,
    description=_("Create a new location.")
)

wizard_pool.register(location_wizard)
