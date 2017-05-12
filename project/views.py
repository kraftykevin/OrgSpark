from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Story, Submission, Story_by_submission, Story_by_paragraph
from .forms import SubmissionForm, UserCreateForm
from django.contrib.auth.models import User
from django.core.mail import send_mail



# home goes to the home page
def home(request):
    all_stories = Story.objects.order_by('popularity').reverse()
    return render(request, 'project/home.html', {'all_stories' : all_stories})

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
    # This function activates a User.
	id=int(request.GET.get('id'))
	user = User.objects.get(id=id)
	user.is_active=True
	user.save()
	return render(request,'registration/activation.html')

def signup(request):
    # This function creates a new user and sends them an activation email.
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



def story(request, slug):
    """
    This function is the story for a page.  It includes rendering the story,
    a place to post new text, and rendering submissions.
    """
    _x = Story.objects.get(slug=slug)
    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.author = request.user
            else:
                _anon = User.objects.get(username="Anonymous")
                post.author = _anon
            post.vote = 1
            post.story = _x
            post.save()
            return redirect('story', slug=slug)
    else:
        form = SubmissionForm()
        _user = request.user.username

        whole_story = Story_by_paragraph.objects.filter(story=_x).order_by('pk')
        #above line orders the model where each object is a paragraph by ID and places it in whole_story variable

        submissions_by_vote = Submission.objects.filter(story=_x).order_by('vote').reverse()
        #all present submissions ordered by number of votes

        #_z = Story_by_submission.objects.filter(story=_x)(author__username=_user).count()
        # _z is the number of accepted submissions for this user
        # would need to figure out how to pass multiple arguments to Django's filter()
        #user_stake = "{0:.2f}%".format((_z / 500)*100)
        # percent of users stake in the story assuming 450 submissions and 50 OrgSpark owned
        # Need to changed based on muse owning some too.

        _y = Story_by_submission.objects.filter(story=_x).count()
        progress = "{0:.2f}%".format((_y / 450) * 100)

        prompt = _x.prompt
        title = _x.title

        # need to re-add in 'user_stake':user_stake, below
        return render(request, 'project/story.html', {'whole_story': whole_story,
        'progress': progress, 'form': form, 'submissions_by_vote': submissions_by_vote,
        'prompt': prompt, 'title': title, 'slug': slug})




def vote(request, Submission_id):
    # This function allows folks to vote.
    if request.user.is_authenticated:
        if Submission.objects.filter(pk=Submission_id).exists():
            _user = request.user
            _x = Submission.objects.get(pk=Submission_id)
            if _x.author != _user:
                _y=_x.story
                slug=_y.slug
                _z=_y.voted
                if _z.filter(id=_user.id).exists():
                    return redirect('alreadyvoted')
                else:
                    _x.vote += 1
                    _x.save()
                    _y.popularity += 1
                    _y.voted.add(_user)
                    _y.save()
                    return redirect('story', slug=slug)
            else:
                return redirect('nicetry')
        else:
            return redirect('home')
            #just in case user clicks vote after Calcvote has occured
    else:
        return redirect('signup1')




"""

def calcvote():
    print("Running Calcvote!")
    x = Suba.objects.order_by('vote').last()
    if x == None:
        return
    elif x.vote < 4: #need at least four votes
        #Suba.objects.filter(vote__lt=x.vote).delete()
        Voted1.objects.all().delete()
        return
    elif Suba.objects.filter(vote=x.vote).count() > 1:
        #Suba.objects.filter(vote__lt=x.vote).delete()
        Voted1.objects.all().delete()
        return
    else:
        Texta.objects.create(text=x.text, author=x.author, vote=x.vote, paragraph=x.paragraph)
        Suba.objects.all().delete()
        Voted1.objects.all().delete()
        lastentry=Texta.objects.order_by('pk').last()
        story1lastentry = Story1.objects.order_by('pk').last()
        zz = Story1.objects.all().count()
        if zz == 0:
            Story1.objects.create(text=lastentry.text)
            return
        elif lastentry.paragraph == True:
            Story1.objects.create(text=lastentry.text)
            return
            #start new story1 object for new paragraph
        else:
            story1lastentry.text=str(story1lastentry.text)+"  "+str(lastentry.text)
            story1lastentry.save()
            return
            # removed z, moved story1lastentry creation up to, and keep zz.



            

def calcvote2():
    print("Running calcvote2")
    x = Subb.objects.order_by('vote').last()
    if x == None:
        return
    elif x.vote < 4: #need at least four votes
        #Subb.objects.filter(vote__lt=x.vote).delete()
        Voted2.objects.all().delete()
        return
    elif Subb.objects.filter(vote=x.vote).count() > 1:
        #Subb.objects.filter(vote__lt=x.vote).delete()
        Voted2.objects.all().delete()
        return
    else:
        Textb.objects.create(text=x.text, author=x.author, vote=x.vote, paragraph=x.paragraph)
        Subb.objects.all().delete()
        Voted2.objects.all().delete()
        lastentry=Textb.objects.order_by('pk').last()
        story2lastentry = Story2.objects.order_by('pk').last()
        zz = Story2.objects.all().count()
        if zz == 0:
            Story2.objects.create(text=lastentry.text)
            return
        elif lastentry.paragraph == True:
            Story2.objects.create(text=lastentry.text)
            return
            #start new story1 object for new paragraph
        else:
            story2lastentry.text=str(story2lastentry.text)+"  "+str(lastentry.text)
            story2lastentry.save()
            return



def calcvote3():
    print("Running calcvote3")
    x = Subc.objects.order_by('vote').last()
    if x == None:
        return
    elif x.vote < 4: #need at least four votes
        #Subc.objects.filter(vote__lt=x.vote).delete()
        Voted3.objects.all().delete()
        return
    elif Subc.objects.filter(vote=x.vote).count() > 1:
        #Subc.objects.filter(vote__lt=x.vote).delete()
        Voted3.objects.all().delete()
        return
    else:
        Textc.objects.create(text=x.text, author=x.author, vote=x.vote, paragraph=x.paragraph)
        Subc.objects.all().delete()
        Voted3.objects.all().delete()
        lastentry=Textc.objects.order_by('pk').last()
        story3lastentry = Story3.objects.order_by('pk').last()
        zz = Story3.objects.all().count()
        if zz == 0:
            Story3.objects.create(text=lastentry.text)
            return
        elif lastentry.paragraph == True:
            Story3.objects.create(text=lastentry.text)
            return
            #start new story1 object for new paragraph
        else:
            story3lastentry.text=str(story3lastentry.text)+"  "+str(lastentry.text)
            story3lastentry.save()
            return



def calcvote4():
    print("Running calcvote4")
    x = Subd.objects.order_by('vote').last()
    if x == None:
        return
    elif x.vote < 4: #need at least four votes
        #Subd.objects.filter(vote__lt=x.vote).delete()
        Voted4.objects.all().delete()
        return
    elif Subd.objects.filter(vote=x.vote).count() > 1:
        #Subd.objects.filter(vote__lt=x.vote).delete()
        Voted4.objects.all().delete()
        return
    else:
        Textd.objects.create(text=x.text, author=x.author, vote=x.vote, paragraph=x.paragraph)
        Subd.objects.all().delete()
        Voted4.objects.all().delete()
        lastentry=Textd.objects.order_by('pk').last()
        story4lastentry = Story4.objects.order_by('pk').last()
        zz = Story4.objects.all().count()
        if zz == 0:
            Story4.objects.create(text=lastentry.text)
            return
        elif lastentry.paragraph == True:
            Story4.objects.create(text=lastentry.text)
            return
            #start new story1 object for new paragraph
        else:
            story4lastentry.text=str(story4lastentry.text)+"  "+str(lastentry.text)
            story4lastentry.save()
            return

"""
