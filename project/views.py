from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Texta, Suba
from .forms import PostForm


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

def story1read(request):
    story1 = Texta.objects.order_by('pk')
    return render(request, 'project/story1read.html', {'story1': story1})

def story1contrib(request):
    suba1 = Suba.objects.order_by('vote').reverse()
    return render(request, 'project/story1.html', {'suba1':suba1})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)   #so do I need to switch out to suba? or is it post
            post.author = request.user
            post.vote = 0
            return redirect('post_detail', pk=suba.pk) #suba or post here???? 
    else:
        form = PostForm()
    return render(request, 'project/submit.html', {'form': form})
