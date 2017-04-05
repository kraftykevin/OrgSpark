from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Texta, Suba, Voted1, Story1
from .forms import SubaForm, UserCreateForm
from django.contrib.auth.models import User
from django.core.mail import send_mail



# home goes to the home page
def home(request):
    return render(request, 'project/home.html', {})

def nicetry(request):
    return render(request, 'project/nicetry.html', {})

def already(request):
    return render(request, 'project/already.html', {})

def alreadyvoted(request):
    return render(request, 'project/alreadyvoted.html', {})

def signup1(request):
    return render(request, 'registration/signup1.html', {})

def signup2(request):
    return render(request, 'registration/signup2.html', {})

def prompt1(request):
    return render(request, 'project/prompt1.html', {})

def already3(request):
    return render(request, 'project/already3.html', {})

def activate(request):
	id=int(request.GET.get('id'))
	user = User.objects.get(id=id)
	user.is_active=True
	user.save()
	return render(request,'registration/activation.html')



#signup process -
def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            _email = form.cleaned_data.get('email')
            if User.objects.filter(email=_email).exists():
                return redirect('already3')
            user.is_active=False
            user.save()
            _thisuser = User.objects.get(username = username)
            id = _thisuser.pk
            send_mail(
                'Welcome to OrgSpark!',
                'Here is the link to activate your OrgSpark account:\nhttp://127.0.0.1:8000/register_activate/activation/?id=%s' %(id),
                'OrgSpark@gmail.com',
                [_email],
                fail_silently=False)
            return redirect ('signup2')
    else:
        form = UserCreateForm()
    return render(request, 'registration/signup.html', {'form': form})




def story1read(request):
    zzz = Story1.objects.order_by('pk')
    _user = request.user.username
    _z = Texta.objects.filter(author__username=_user).count()
    stake1 = "{0:.2f}%".format((_z / 500)*100)
    _y = Texta.objects.count()
    progress1 =    "{0:.2f}%".format((_y / 450) * 100)
    return render(request, 'project/story1read.html', {'zzz': zzz, 'stake1': stake1, 'progress1': progress1})



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
    elif x.vote < 4: #need at least four votes
        Suba.objects.filter(vote__lt=x.vote).delete()
        Voted1.objects.all().delete()
    elif Suba.objects.filter(vote=x.vote).count() > 1:
        Suba.objects.filter(vote__lt=x.vote).delete()
        Voted1.objects.all().delete()
    else:
        Texta.objects.create(text=x.text, author=x.author, vote=x.vote, paragraph=x.paragraph)
        Suba.objects.all().delete()
        Voted1.objects.all().delete()
        # figure out how to add to pararaph model Story1

        z = Texta.objects.all().count()
        lastentry=Texta.objects.get(pk=z)
        zz = Story1.objects.all().count()
        if zz == 0:
            Story1.objects.create(text=lastentry.text)
            return
        story1lastentry=Story1.objects.get(pk=zz)
        if lastentry.paragraph == True:
            Story1.objects.create(text=lastentry.text)
            #start new story1 object for new paragraph
        else:
            story1lastentry.text=str(story1lastentry.text)+"  "+str(lastentry.text)
            story1lastentry.save()


sched.add_job(calcvote1, 'cron', minute='31')
sched.start()



def vote1(request, suba_id):
    if request.user.is_authenticated:
        if Suba.objects.filter(pk=suba_id).exists():
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
                    return redirect('alreadyvoted')
            else:
                return redirect('nicetry')
        else:
            return redirect('story1')
    else:
        return redirect('signup1')
