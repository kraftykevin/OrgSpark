from django.forms import ModelForm, Textarea, CheckboxInput, EmailField
from .models import Suba
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class SubaForm(ModelForm):
    class Meta:
        model = Suba
        fields = ('text', 'paragraph',)
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 10}),
            'paragraph': CheckboxInput()
        }



class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
