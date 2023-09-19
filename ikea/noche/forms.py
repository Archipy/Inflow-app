from django import forms
from .models import AltaRotacionCheck

class ArchivosForm(forms.Form):
    file1 = forms.FileField(label='PROPUESTA FINAL', widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-sm'}),required=False)
    file2 = forms.FileField(label='PLAN DE DESCARGA', widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-sm'}),required=False)
    file3 = forms.FileField(label='SG010', widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-sm'}),required=False)

class AltaRotacionCheckForm(forms.ModelForm):
    class Meta:
        model = AltaRotacionCheck
        fields = ['lv_checked', 'bajado_checked']  