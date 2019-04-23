from aldryn_client import forms

class Form(forms.BaseForm):
    enable_dx = forms.CheckboxField(
        "Enable DX",
        required=False,
        initial=True)

    def to_settings(self, data, settings):

        if data['enable_dx']:
            settings['LOCATIONS_ENABLE_DX'] = int(data['enable_dx'])


        return settings
