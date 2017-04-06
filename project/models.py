from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Texta(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.CharField(max_length=250)
    vote = models.IntegerField(default=0)
    paragraph = models.BooleanField(default=False)
    # using pk value for num added
    def __str__(self):
        return self.text

class Suba(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.CharField(max_length=250)
    vote = models.IntegerField()
    paragraph = models.BooleanField(default=False)

class Voted1(models.Model):
    voter = models.ForeignKey('auth.User')
    voted = models.BooleanField(default=False)

class Story1(models.Model):
    text = models.TextField()
    def __str__(self):
        return self.text



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
