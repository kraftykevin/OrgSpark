from django.forms import ModelForm, Textarea, CheckboxInput
from .models import Suba


class SubaForm(ModelForm):
    class Meta:
        model = Suba
        fields = ('text', 'newpar',)
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 10}),
            'newpar': CheckboxInput()
        }
