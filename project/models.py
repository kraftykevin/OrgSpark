from django.db import models
from django.contrib.auth.models import User



class Story(models.Model):
    title = models.CharField('title', max_length=100)
    muse = models.ForeignKey('auth.User', related_name = 'muse')
    prompt = models.CharField(max_length=1000)
    slug = models.SlugField('slug', max_length=100, unique=True)
    popularity = models.IntegerField()
    voted = models.ManyToManyField('auth.User', related_name = 'voted')
    #minimum_votes = models.IntegerField()
    #vote_frequency = models.IntegerField()
    #max_submission_length = models.IntegerField() - would need to give max/min int
    #popularity (for ranking on front page)


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

"""
class Voted(models.Model):
    voter = models.ForeignKey('auth.User')
    voted = models.BooleanField(default=False)
    story = models.ForeignKey(Story)
"""
