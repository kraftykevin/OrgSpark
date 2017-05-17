from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Story, Submission, Story_by_submission, Story_by_paragraph
from .forms import SubmissionForm, UserCreateForm, New_story_form
from django.contrib.auth.models import User
from django.core.mail import send_mail
import datetime
from django.template.defaultfilters import slugify



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
        if form.is_valid(): #it appears no else to go with this if, need an error page?
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
        accepted_submissions = Story_by_submission.objects.filter(story=_x).filter(author__username=_user).count()


        user_stake = "{0:.2f}%".format((accepted_submissions / 500)*100)

        # percent of users stake in the story assuming 450 submissions and 50 OrgSpark owned
        # Need to changed based on muse owning some too.
        _y = Story_by_submission.objects.filter(story=_x).count()
        progress = "{0:.2f}%".format((_y / 450) * 100)
        story = _x
        # need to re-add in 'user_stake':user_stake, below
        return render(request, 'project/story.html', {'whole_story': whole_story,
        'progress': progress, 'form': form, 'submissions_by_vote': submissions_by_vote,
         'slug': slug, 'story': story, 'user_stake': user_stake})




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





def newstory(request):
    if request.method == "POST":
        form = New_story_form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.muse = request.user
            slug = slugify(post.title)
            post.slug = slug
            post.save()
            return redirect('story', slug=slug)
        else:
            return redirect('newstory1')
    else:
        if request.user.is_authenticated:
            form = New_story_form()
            return render (request, 'project/newstory.html', {'form': form})
        else:
            return redirect('signup1')

def newstory1(request):
    if request.method == "POST":
        form = New_story_form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.muse = request.user
            slug = slugify(post.title)
            post.slug = slug
            post.save()
            return redirect('story', slug=slug)
        else:
            return redirect('newstory1')
    else:
        if request.user.is_authenticated:
            form = New_story_form()
            return render (request, 'project/newstory1.html', {'form': form})
        else:
            return redirect('signup1')






def calcvote(pk):
    calcvote_story = Story.objects.get(pk=pk)
    _slug = calcvote_story.slug
    now = datetime.datetime.now()
    print("Running Calcvote", _slug, "at", datetime.time(now.hour, now.minute, now.second))
    most_votes = Submission.objects.filter(story=calcvote_story).order_by('vote').last()
    calcvote_minimum_votes = calcvote_story.minimum_votes
    if most_votes == None:
        return
    elif Submission.objects.filter(vote=most_votes.vote).count() > 1:
        calcvote_story.voted.clear()
        return
    elif most_votes.vote <= calcvote_minimum_votes:
        calcvote_story.voted.clear()
        return
    else:
        calcvote_story.voted.clear()
        Story_by_submission.objects.create(text=most_votes.text, author=most_votes.author, vote=most_votes.vote, paragraph=most_votes.paragraph, story=calcvote_story)
        Submission.objects.filter(story=calcvote_story).delete()
        last_entry = Story_by_submission.objects.filter(story=calcvote_story).order_by('pk').last()
        last_paragraph = Story_by_paragraph.objects.filter(story=calcvote_story).order_by('pk').last()
        _z = Story_by_paragraph.objects.filter(story=calcvote_story).count()
        if _z == 0:
            Story_by_paragraph.objects.create(text=last_entry.text, story=calcvote_story)
            return
        elif last_entry.paragraph == True:
            Story_by_paragraph.objects.create(text=lastentry.text, story=calcvote_story)
            return
        else:
            last_paragraph.text=str(last_paragraph.text)+"  "+str(last_entry.text)
            last_paragraph.save()
            return
