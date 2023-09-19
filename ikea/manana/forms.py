from django import forms
from .models import Outs

class OutsForm(forms.ModelForm):
    class Meta:
        model = Outs
        fields = ['code', 'ubicacion', 'puertas','motivo', 'down']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-inline outs-apertura','style': 'margin: 5px;','placeholder': 'Referencia'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-inline outs-apertura','style': 'margin: 5px;','placeholder': 'Ubicación'}),
            'puertas': forms.Select(attrs={'class': 'form-inline outs-apertura','style': 'margin: 5px;'}),
            'motivo': forms.Select(attrs={'class': 'form-inline outs-apertura','style': 'margin: 5px;'}),
            'down': forms.CheckboxInput(attrs={'class': 'form-inline outs-apertura','style': 'margin: 5px;'}),
        }