from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator



class Story(models.Model):
    title = models.CharField('title', max_length=100, unique=True)
    muse = models.ForeignKey('auth.User', related_name = 'muse')
    prompt = models.CharField(max_length=1000)
    slug = models.SlugField('slug', max_length=100, unique=True)
    popularity = models.IntegerField()
    voted = models.ManyToManyField('auth.User', related_name = 'voted')
    finished_story = models.BooleanField(default=False)
    vote_minimum = models.IntegerField(validators=[MinValueValidator(3), MaxValueValidator(100)])
    vote_frequency = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(1440)])


class Submission(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.CharField(max_length=250)
    vote = models.IntegerField()
    paragraph = models.BooleanField(default=False)
    story = models.ForeignKey(Story)


class Story_by_submission(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.CharField(max_length=250)
    vote = models.IntegerField(default=0)
    paragraph = models.BooleanField(default=False)
    story = models.ForeignKey(Story)
    def __str__(self):
        return self.text


class Story_by_paragraph(models.Model):
    text = models.TextField()
    story = models.ForeignKey(Story)
    def __str__(self):
        return self.text
