from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Texta, Suba
from .forms import SubaForm


# home goes to the home page
def home(request):
    return render(request, 'project/home.html', {})



def signup1(request):
    return render(request, 'registration/signup1.html', {})

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

def story1read(request):
    story1 = Texta.objects.order_by('pk')
    return render(request, 'project/story1read.html', {'story1': story1})


def story1contrib(request):
    suba1 = Suba.objects.order_by('vote').reverse()
    return render(request, 'project/story1.html', {'suba1':suba1})



def story1submit(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = SubaForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.vote = 0
                post.save()
            return redirect('story1')
        else:
            return redirect('signup1')
    else:
        form = SubaForm()
    return render(request, 'project/story1submit.html', {'form': form})
