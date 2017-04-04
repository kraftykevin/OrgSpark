from django.forms import ModelForm, Textarea
from .models import Suba


class SubaForm(ModelForm):
    class Meta:
        model = Suba
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 10}),
        }
