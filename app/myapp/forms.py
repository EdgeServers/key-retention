from django import forms
from .models import Driver, KeyHanger

class ArrivalForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ('name', 'truck_rego_number', 'key_hanger_number', 'parking_location', 'rear_wheel_chocked', 'key_removed_from_ignition')

    def __init__(self, *args, **kwargs):
        super(ArrivalForm, self).__init__(*args, **kwargs)
        self.fields['key_hanger_number'].queryset = KeyHanger.objects.filter(is_available=True)

class DepartureForm(forms.Form):
    driver = forms.ModelChoiceField(queryset=Driver.objects.filter(departure_time__isnull=True))
    key_hanger_number = forms.CharField(widget=forms.HiddenInput(), required=False)
    take_key = forms.BooleanField(required=False)
