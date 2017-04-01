from django import forms
from django.db import models
from .models import Suba

class PostForm(forms.ModelForm):
    class Meta:
        model = Suba
        fields = ('text',)
