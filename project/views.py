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
                #if Voted1.objects.filter(voter=_user).exists()==False:
                    _x.vote += 1
                    _x.save()
                    #Voted1.objects.create(voter=_user, voted=True)
                    _y=_x.story
                    slug=_y.slug
                    return redirect('story', slug=slug)
                #else:
                    #return redirect('alreadyvoted')
            else:
                return redirect('nicetry')
        else:
            return redirect('home') #just in case user clicks vote after Calcvote has occured
    else:
        return redirect('signup1')







"""


# everything past here is just copy code, figure out how to dry it out!

def story2(request):

    #This function is the story for a page.  It includes rendering the story,
    #a place to post new text, and rendering submissions.

    if request.method == "POST":
        #if request.user.is_authenticated:
        # Uncomment above line to make it so only logged in users can post
                #xyz=request.user
            #if Suba.objects.filter(author=xyz).exists()==False:
                form = SubbForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    if request.user.is_authenticated:
                        post.author = request.user
                    else:
                        _x = User.objects.get(username="Anonymous")
                        post.author = _x
                    post.vote = 1
                    post.save()
                    return redirect('story2')
            #else:
                #return redirect('already')
        #else:
            #return redirect('signup1')
            # uncomment above line to make it so only logged in users can post
    else:
        form = SubbForm()
        whole_story = Story2.objects.order_by('pk')
        #above line orders the model where each object is a paragraph by ID and places it in whole_story variable
        _user = request.user.username
        _z = Textb.objects.filter(author__username=_user).count()
        # _z is the number of accepted submissions for this user
        user_stake = "{0:.2f}%".format((_z / 500)*100)
        # percent of users stake in the story assuming 450 submissions and 50 OrgSpark owned
        _y = Textb.objects.count()
        # Number of total accepted submissions so far
        progress = "{0:.2f}%".format((_y / 450) * 100)
        submissions_by_vote = Subb.objects.order_by('vote').reverse()
        #all present submissions ordered by number of votes
        return render(request, 'project/story2.html', {'whole_story': whole_story, 'user_stake': user_stake, 'progress': progress, 'form': form, 'submissions_by_vote': submissions_by_vote})



def story3(request):

    #This function is the story for a page.  It includes rendering the story,
    #a place to post new text, and rendering submissions.
    if request.method == "POST":
        #if request.user.is_authenticated:
        # Uncomment above line to make it so only logged in users can post
                #xyz=request.user
            #if Suba.objects.filter(author=xyz).exists()==False:
                form = SubcForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    if request.user.is_authenticated:
                        post.author = request.user
                    else:
                        _x = User.objects.get(username="Anonymous")
                        post.author = _x
                    post.vote = 1
                    post.save()
                    return redirect('story3')
            #else:
                #return redirect('already')
        #else:
            #return redirect('signup1')
            # uncomment above line to make it so only logged in users can post
    else:
        form = SubcForm()
        whole_story = Story3.objects.order_by('pk')
        #above line orders the model where each object is a paragraph by ID and places it in whole_story variable
        _user = request.user.username
        _z = Textc.objects.filter(author__username=_user).count()
        # _z is the number of accepted submissions for this user
        user_stake = "{0:.2f}%".format((_z / 500)*100)
        # percent of users stake in the story assuming 450 submissions and 50 OrgSpark owned
        _y = Textc.objects.count()
        # Number of total accepted submissions so far
        progress = "{0:.2f}%".format((_y / 450) * 100)
        submissions_by_vote = Subc.objects.order_by('vote').reverse()
        #all present submissions ordered by number of votes
        return render(request, 'project/story3.html', {'whole_story': whole_story, 'user_stake': user_stake, 'progress': progress, 'form': form, 'submissions_by_vote': submissions_by_vote})



def story4(request):

    #This function is the story for a page.  It includes rendering the story,
    #a place to post new text, and rendering submissions.

    if request.method == "POST":
        #if request.user.is_authenticated:
        # Uncomment above line to make it so only logged in users can post
                #xyz=request.user
            #if Suba.objects.filter(author=xyz).exists()==False:
                form = SubdForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    if request.user.is_authenticated:
                        post.author = request.user
                    else:
                        _x = User.objects.get(username="Anonymous")
                        post.author = _x
                    post.vote = 1
                    post.save()
                    return redirect('story4')
            #else:
                #return redirect('already')
        #else:
            #return redirect('signup1')
            # uncomment above line to make it so only logged in users can post
    else:
        form = SubdForm()
        whole_story = Story4.objects.order_by('pk')
        #above line orders the model where each object is a paragraph by ID and places it in whole_story variable
        _user = request.user.username
        _z = Textd.objects.filter(author__username=_user).count()
        # _z is the number of accepted submissions for this user
        user_stake = "{0:.2f}%".format((_z / 500)*100)
        # percent of users stake in the story assuming 450 submissions and 50 OrgSpark owned
        _y = Textd.objects.count()
        # Number of total accepted submissions so far
        progress =    "{0:.2f}%".format((_y / 450) * 100)
        submissions_by_vote = Subd.objects.order_by('vote').reverse()
        #all present submissions ordered by number of votes
        return render(request, 'project/story4.html', {'whole_story': whole_story, 'user_stake': user_stake, 'progress': progress, 'form': form, 'submissions_by_vote': submissions_by_vote})


"""

# -------------------------------------------

"""


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


"""

#________________________________

"""
def calcvote1():
    print("Running calcvote1")
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
