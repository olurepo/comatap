from django import forms
from .models import TestConfig

class TestConfiguration(forms.ModelForm):
    class Meta:
        model = TestConfig
        fields = [
            'datum_temp',
            'activation_energy',
            'gas_constant',
            'ref_temp',
            'ultimate_strength',
            'a',
            'b',
            'sensor',
        ]


class MaturityForm(forms.Form):
    datum_temp = forms.FloatField(widget=forms.Textarea(attrs={
        'placeholder': 'default: -10',
    }))
    activation_energy = forms.FloatField(widget=forms.Textarea(attrs={
        'placeholder': 'default: 40,000',
    }))
    gas_constant = forms.FloatField()
    ref_temp = forms.FloatField()
    ultimate_strength = forms.FloatField()
    a = forms.FloatField()
    b = forms.FloatField()