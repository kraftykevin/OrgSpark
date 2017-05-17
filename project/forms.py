from django.forms import ModelForm, Textarea, CheckboxInput, EmailField
from .models import Submission, Story
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



class New_story_form(ModelForm):
    class Meta:
        model = Story
        fields = ('title', 'prompt', 'minimum_votes', 'minutes_between_votes')
        widgets = {
            'title': Textarea(attrs={'cols': 80, 'rows': 2}),
            'prompt': Textarea(attrs={'cols': 80, 'rows': 10}),
            'minimum_votes': Textarea(attrs={'cols': 80, 'rows': 2}),
            'minutes_between_votes': Textarea(attrs={'cols': 80, 'rows': 2}),
        }
