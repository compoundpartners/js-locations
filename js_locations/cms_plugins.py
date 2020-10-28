# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template import TemplateDoesNotExist
from django.template.loader import select_template

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from sortedm2m_filter_horizontal_widget.forms import SortedFilteredSelectMultiple, SortedMultipleChoiceField

from . import models
from .constants import SPECIFIC_LOCATIONS_LAYOUTS


class SpecificLocationsPluginForm(forms.ModelForm):
    layout = forms.ChoiceField(choices=SPECIFIC_LOCATIONS_LAYOUTS, required=False)
    locations = SortedMultipleChoiceField(
        label='locations',
        queryset=models.Location.objects.all(),
        required=False,
        widget=SortedFilteredSelectMultiple(attrs={'verbose_name':'location', 'verbose_name_plural':'locations'})
    )


@plugin_pool.register_plugin
class SpecificLocationsPlugin(CMSPluginBase):
    render_template = 'js_locations/plugins/locations.html'
    TEMPLATE_NAME = 'js_locations/plugins/locations_%s.html'
    name = _('Specific Locations')
    model = models.SpecificLocationsPlugin
    form = SpecificLocationsPluginForm
    fields = [
        'title',
        'layout',
        'more_button_is_shown',
        'more_button_text',
        'more_button_link',
        'locations',
    ]

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['title'] = instance.title
        context['more_button_is_shown'] = instance.more_button_is_shown
        context['more_button_text'] = instance.more_button_text
        context['more_button_link'] = instance.more_button_link
        if instance.locations.count():
            context['locations'] = instance.locations.all()
        return context

    def get_render_template(self, context, instance, placeholder):
        if instance.layout:
            template = self.TEMPLATE_NAME % instance.layout
            try:
                select_template([template])
                return template
            except TemplateDoesNotExist:
                pass
        return self.render_template
