from django import forms
from .models import Suba


class SubaForm(forms.ModelForm):
    class Meta:
        model = Suba
        fields = ('text',)  #is this comma supposed to be here...?
