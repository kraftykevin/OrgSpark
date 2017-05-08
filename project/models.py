from django.db import models
from django.contrib.auth.models import User



class Story(models.Model):
    title = models.CharField('title', max_length=100)
    muse = models.ForeignKey('auth.User')
    prompt = models.CharField(max_length=1000)
    slug = models.SlugField('slug', max_length=100, unique=True)
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
    # using pk value for num added
    def __str__(self):
        return self.text


class Story_by_paragraph(models.Model):
    text = models.TextField()
    story = models.ForeignKey(Story)
    def __str__(self):
        return self.text


class Voted(models.Model):
    voter = models.ForeignKey('auth.User')
    voted = models.BooleanField(default=False)
    story = models.ForeignKey(Story)


"""

#  Everything after this is bad copy code - DRY all this out!!!

class Textb(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.CharField(max_length=250)
    vote = models.IntegerField(default=0)
    paragraph = models.BooleanField(default=False)
    # using pk value for num added
    def __str__(self):
        return self.text

class Subb(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.CharField(max_length=250)
    vote = models.IntegerField()
    paragraph = models.BooleanField(default=False)

class Voted2(models.Model):
    voter = models.ForeignKey('auth.User')
    voted = models.BooleanField(default=False)

class Story2(models.Model):
    text = models.TextField()
    def __str__(self):
        return self.text

#-----------

class Textc(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.CharField(max_length=250)
    vote = models.IntegerField(default=0)
    paragraph = models.BooleanField(default=False)
    # using pk value for num added
    def __str__(self):
        return self.text

class Subc(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.CharField(max_length=250)
    vote = models.IntegerField()
    paragraph = models.BooleanField(default=False)

class Voted3(models.Model):
    voter = models.ForeignKey('auth.User')
    voted = models.BooleanField(default=False)

class Story3(models.Model):
    text = models.TextField()
    def __str__(self):
        return self.text




#-=-------------------------

class Textd(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.CharField(max_length=250)
    vote = models.IntegerField(default=0)
    paragraph = models.BooleanField(default=False)
    # using pk value for num added
    def __str__(self):
        return self.text

class Subd(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.CharField(max_length=250)
    vote = models.IntegerField()
    paragraph = models.BooleanField(default=False)

class Voted4(models.Model):
    voter = models.ForeignKey('auth.User')
    voted = models.BooleanField(default=False)

class Story4(models.Model):
    text = models.TextField()
    def __str__(self):
        return self.text
"""
