from django import forms
from .models import Location


class UploadForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = ['place', 'population']
