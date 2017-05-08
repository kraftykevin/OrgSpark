from django.forms import ModelForm, Textarea, CheckboxInput, EmailField
from .models import Submission
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms




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

class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ('text', 'paragraph',)
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 10}),
            'paragraph': CheckboxInput()
        }



# copy paste code past this point.  DRY out.

"""
class SubbForm(ModelForm):
    class Meta:
        model = Subb
        fields = ('text', 'paragraph',)
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 10}),
            'paragraph': CheckboxInput()
        }

class SubcForm(ModelForm):
    class Meta:
        model = Subc
        fields = ('text', 'paragraph',)
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 10}),
            'paragraph': CheckboxInput()
        }

class SubdForm(ModelForm):
    class Meta:
        model = Subd
        fields = ('text', 'paragraph',)
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 10}),
            'paragraph': CheckboxInput()
        }

"""
