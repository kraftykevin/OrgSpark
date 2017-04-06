from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Texta, Textb, Textc, Textd, Suba, Subb, Subc, Subd, Voted1, Voted2, Voted3, Voted4, Story1, Story2, Story3, Story4
from .forms import SubaForm, SubbForm, SubcForm, SubdForm, UserCreateForm
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


def already3(request):
    return render(request, 'project/already3.html', {})

def activate(request):
	id=int(request.GET.get('id'))
	user = User.objects.get(id=id)
	user.is_active=True
	user.save()
	return render(request,'registration/activation.html')


def prompt1(request):
    return render(request, 'project/prompt1.html', {})

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
                'Here is the link to activate your OrgSpark account:\nhttp:www.orgspark.com/register_activate/activation/?id=%s' %(id),
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
        return
    elif Suba.objects.filter(vote=x.vote).count() > 1:
        Suba.objects.filter(vote__lt=x.vote).delete()
        Voted1.objects.all().delete()
        return
    else:
        Texta.objects.create(text=x.text, author=x.author, vote=x.vote, paragraph=x.paragraph)
        Suba.objects.all().delete()
        Voted1.objects.all().delete()
        z = Texta.objects.all().count()
        lastentry=Texta.objects.get(pk=z)
        zz = Story1.objects.all().count()
        if zz == 0:
            Story1.objects.create(text=lastentry.text)
            return
        story1lastentry = Story1.objects.get(pk=zz)
        if lastentry.paragraph == True:
            Story1.objects.create(text=lastentry.text)
            return
            #start new story1 object for new paragraph
        else:
            story1lastentry.text=str(story1lastentry.text)+"  "+str(lastentry.text)
            story1lastentry.save()
            return






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




# everything past here is just copy code, figure out how to dry it out!

def story2read(request):
    zzz = Story2.objects.order_by('pk')
    _user = request.user.username
    _z = Textb.objects.filter(author__username=_user).count()
    stake2 = "{0:.2f}%".format((_z / 500)*100)
    _y = Textb.objects.count()
    progress2 =    "{0:.2f}%".format((_y / 450) * 100)
    return render(request, 'project/story2read.html', {'zzz': zzz, 'stake2': stake2, 'progress2': progress2})

def story3read(request):
    zzz = Story3.objects.order_by('pk')
    _user = request.user.username
    _z = Textc.objects.filter(author__username=_user).count()
    stake3 = "{0:.2f}%".format((_z / 500)*100)
    _y = Textc.objects.count()
    progress3 =    "{0:.2f}%".format((_y / 450) * 100)
    return render(request, 'project/story3read.html', {'zzz': zzz, 'stake3': stake3, 'progress3': progress3})

def story4read(request):
    zzz = Story4.objects.order_by('pk')
    _user = request.user.username
    _z = Textd.objects.filter(author__username=_user).count()
    stake4 = "{0:.2f}%".format((_z / 500)*100)
    _y = Textd.objects.count()
    progress4 =    "{0:.2f}%".format((_y / 450) * 100)
    return render(request, 'project/story4read.html', {'zzz': zzz, 'stake4': stake4, 'progress4': progress4})

#------------------------------------

def story2contrib(request):
    subb2 = Subb.objects.order_by('vote').reverse()
    return render(request, 'project/story2.html', {'subb2':subb2})

def story3contrib(request):
    subc3 = Subc.objects.order_by('vote').reverse()
    return render(request, 'project/story3.html', {'subc3':subc3})

def story4contrib(request):
    subd4 = Subd.objects.order_by('vote').reverse()
    return render(request, 'project/story4.html', {'subd4':subd4})


# -----------------------------------------

def story2submit(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            xyz=request.user
            if Subb.objects.filter(author=xyz).exists()==False:
                form = SubbForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.author = request.user
                    post.vote = 0
                    post.save()
                    return redirect('story2')
            else:
                return redirect('already')
        else:
            return redirect('signup1')
    else:
        form = SubbForm()
    return render(request, 'project/story2submit.html', {'form': form})



def story3submit(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            xyz=request.user
            if Subc.objects.filter(author=xyz).exists()==False:
                form = SubcForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.author = request.user
                    post.vote = 0
                    post.save()
                    return redirect('story3')
            else:
                return redirect('already')
        else:
            return redirect('signup1')
    else:
        form = SubcForm()
    return render(request, 'project/story3submit.html', {'form': form})



def story4submit(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            xyz=request.user
            if Subd.objects.filter(author=xyz).exists()==False:
                form = SubdForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.author = request.user
                    post.vote = 0
                    post.save()
                    return redirect('story4')
            else:
                return redirect('already')
        else:
            return redirect('signup1')
    else:
        form = SubdForm()
    return render(request, 'project/story4submit.html', {'form': form})

# -----------------------------------------------------------

def calcvote2():
    x = Subb.objects.order_by('vote').last()
    if x == None:
        return
    elif x.vote < 4: #need at least four votes
        Subb.objects.filter(vote__lt=x.vote).delete()
        Voted2.objects.all().delete()
        return
    elif Subb.objects.filter(vote=x.vote).count() > 1:
        Subb.objects.filter(vote__lt=x.vote).delete()
        Voted2.objects.all().delete()
        return
    else:
        Textb.objects.create(text=x.text, author=x.author, vote=x.vote, paragraph=x.paragraph)
        Subb.objects.all().delete()
        Voted2.objects.all().delete()
        z = Textb.objects.all().count()
        lastentry=Textb.objects.get(pk=z)
        zz = Story2.objects.all().count()
        if zz == 0:
            Story2.objects.create(text=lastentry.text)
            return
        story2lastentry = Story2.objects.get(pk=zz)
        if lastentry.paragraph == True:
            Story2.objects.create(text=lastentry.text)
            return
            #start new story1 object for new paragraph
        else:
            story2lastentry.text=str(story2lastentry.text)+"  "+str(lastentry.text)
            story2lastentry.save()
            return



def calcvote3():
    x = Subc.objects.order_by('vote').last()
    if x == None:
        return
    elif x.vote < 4: #need at least four votes
        Subc.objects.filter(vote__lt=x.vote).delete()
        Voted3.objects.all().delete()
        return
    elif Subc.objects.filter(vote=x.vote).count() > 1:
        Subc.objects.filter(vote__lt=x.vote).delete()
        Voted3.objects.all().delete()
        return
    else:
        Textc.objects.create(text=x.text, author=x.author, vote=x.vote, paragraph=x.paragraph)
        Subc.objects.all().delete()
        Voted3.objects.all().delete()
        z = Textc.objects.all().count()
        lastentry=Textc.objects.get(pk=z)
        zz = Story3.objects.all().count()
        if zz == 0:
            Story3.objects.create(text=lastentry.text)
            return
        story3lastentry = Story3.objects.get(pk=zz)
        if lastentry.paragraph == True:
            Story3.objects.create(text=lastentry.text)
            return
            #start new story1 object for new paragraph
        else:
            story3lastentry.text=str(story3lastentry.text)+"  "+str(lastentry.text)
            story3lastentry.save()
            return



def calcvote4():
    x = Subd.objects.order_by('vote').last()
    if x == None:
        return
    elif x.vote < 4: #need at least four votes
        Subd.objects.filter(vote__lt=x.vote).delete()
        Voted4.objects.all().delete()
        return
    elif Subd.objects.filter(vote=x.vote).count() > 1:
        Subd.objects.filter(vote__lt=x.vote).delete()
        Voted4.objects.all().delete()
        return
    else:
        Textd.objects.create(text=x.text, author=x.author, vote=x.vote, paragraph=x.paragraph)
        Subd.objects.all().delete()
        Voted4.objects.all().delete()
        z = Textd.objects.all().count()
        lastentry=Textd.objects.get(pk=z)
        zz = Story4.objects.all().count()
        if zz == 0:
            Story4.objects.create(text=lastentry.text)
            return
        story4lastentry = Story4.objects.get(pk=zz)
        if lastentry.paragraph == True:
            Story4.objects.create(text=lastentry.text)
            return
            #start new story1 object for new paragraph
        else:
            story4lastentry.text=str(story4lastentry.text)+"  "+str(lastentry.text)
            story4lastentry.save()
            return

sched.add_job(calcvote1, 'cron', minute='00')
sched.add_job(calcvote2, 'cron', minute='15')
sched.add_job(calcvote3, 'cron', minute='30')
sched.add_job(calcvote4, 'cron', minute='45')
sched.start()

# -------------------------------------------

def vote2(request, subb_id):
    if request.user.is_authenticated:
        if Subb.objects.filter(pk=subb_id).exists():
            xyz = request.user
            subbs = Subb.objects.get(pk=subb_id)
            if subbs.author != xyz:
                if Voted2.objects.filter(voter=xyz).exists()==False:
                    subb = Subb.objects.get(pk=subb_id)
                    subb.vote += 1
                    subb.save()
                    Voted2.objects.create(voter=xyz, voted=True)
                    return redirect('story2')
                else:
                    return redirect('alreadyvoted')
            else:
                return redirect('nicetry')
        else:
            return redirect('story2')
    else:
        return redirect('signup1')




def vote3(request, subc_id):
    if request.user.is_authenticated:
        if Subc.objects.filter(pk=subc_id).exists():
            xyz = request.user
            subcs = Subc.objects.get(pk=subc_id)
            if subcs.author != xyz:
                if Voted3.objects.filter(voter=xyz).exists()==False:
                    subc = Subc.objects.get(pk=subc_id)
                    subc.vote += 1
                    subc.save()
                    Voted3.objects.create(voter=xyz, voted=True)
                    return redirect('story3')
                else:
                    return redirect('alreadyvoted')
            else:
                return redirect('nicetry')
        else:
            return redirect('story3')
    else:
        return redirect('signup1')


def vote4(request, subd_id):
    if request.user.is_authenticated:
        if Subd.objects.filter(pk=subd_id).exists():
            xyz = request.user
            subds = Subd.objects.get(pk=subd_id)
            if subds.author != xyz:
                if Voted4.objects.filter(voter=xyz).exists()==False:
                    subd = Subd.objects.get(pk=subd_id)
                    subd.vote += 1
                    subd.save()
                    Voted4.objects.create(voter=xyz, voted=True)
                    return redirect('story4')
                else:
                    return redirect('alreadyvoted')
            else:
                return redirect('nicetry')
        else:
            return redirect('story4')
    else:
        return redirect('signup1')

#-------------------------------------------




def prompt2(request):
    return render(request, 'project/prompt2.html', {})

def prompt3(request):
    return render(request, 'project/prompt3.html', {})

def prompt4(request):
    return render(request, 'project/prompt4.html', {})
