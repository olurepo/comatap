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
        'rows': '1', # this is the size of the input box
    }))
    
    activation_energy = forms.FloatField(widget=forms.Textarea(attrs={
        'placeholder': 'default: 40,000',
        'rows': '1',
    }))

    gas_constant = forms.FloatField(widget=forms.Textarea(attrs={
        'placeholder': 'default: 8.314',
        'rows': '1',
    }))

    ref_temp = forms.FloatField(widget=forms.Textarea(attrs={
        'placeholder': 'default: 23.0°C',
        'rows': '1',
    }))

    ultimate_strength = forms.FloatField(widget=forms.Textarea(attrs={
        'placeholder': 'default: 50MPa',
        'rows': '1',
    }))

    a = forms.FloatField(widget=forms.Textarea(attrs={
        'placeholder': 'default: 4.0',
        'rows': '1',
    }))

    b = forms.FloatField(widget=forms.Textarea(attrs={
        'placeholder': 'default: 0.85',
        'rows': '1',
    }))