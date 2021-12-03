from aldryn_client import forms

class Form(forms.BaseForm):
    enable_dx = forms.CheckboxField(
        "Enable DX",
        required=False,
        initial=False)
    enable_currencies = forms.CheckboxField(
        "Enable Currencies Accepted",
        required=False,
        initial=False)

    def to_settings(self, data, settings):

        settings['LOCATIONS_ENABLE_DX'] = int(data['enable_dx'])
        settings['LOCATIONS_ENABLE_CURRENCIES'] = int(data['enable_currencies'])


        return settings
