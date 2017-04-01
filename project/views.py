from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Texta


# home goes to the home page
def home(request):
    return render(request, 'project/home.html', {})

#signup process -
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def story1contrib(request):
    return render(request, 'project/story1.html', {})

def story1read(request):
    story1 = Texta.objects.order_by('pk')
    return render(request, 'project/story1read.html', {'story1': story1})
