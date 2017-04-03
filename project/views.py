from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Texta, Suba, Voted1
from .forms import SubaForm


# home goes to the home page
def home(request):
    return render(request, 'project/home.html', {})

def nicetry(request):
    return render(request, 'project/nicetry.html', {})

def already(request):
    return render(request, 'project/already.html', {})

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


#Posting Text
def story1submit(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            xyz=request.user
            if Suba.objects.filter(author=xyz).exists()==False:
                form = SubaForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.author = request.user
                    post.vote = 0
                    post.save()
                    return redirect('story1')
            else:
                return redirect('already')
        else:
            return redirect('signup1')
    else:
        form = SubaForm()
    return render(request, 'project/story1submit.html', {'form': form})





from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()

def calcvote1():
    x = Suba.objects.order_by('vote').last()
    if x == None:
        return
    elif x.vote < 3: #need at least four votes
        Suba.objects.filter(vote__lt=x.vote).delete()
        Voted1.objects.all().delete()
    elif Suba.objects.filter(vote=x.vote).count() > 1:
        Suba.objects.filter(vote__lt=x.vote).delete()
        Voted1.objects.all().delete()
    else:
        Texta.objects.create(text=x.text, author=x.author, vote=x.vote)
        Suba.objects.all().delete()
        Voted1.objects.all().delete()

sched.add_job(calcvote1, 'cron', minute='58')
sched.start()



def vote1(request, suba_id):
    if request.user.is_authenticated:
        xyz = request.user
        subas = Suba.objects.get(pk=suba_id)
        if subas.author != xyz:
            if Voted1.objects.filter(voter=xyz).exists()==False:
                suba = Suba.objects.get(pk=suba_id)
                suba.vote += 1
                suba.save()
                Voted1.objects.create(voter=xyz, voted=True)
                return redirect('story1')
            else:
                return redirect('already')
        else:
            return redirect('nicetry')
    else:
        return redirect('signup1')
