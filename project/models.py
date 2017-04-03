from django.db import models

# Create your models here.

class Texta(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.CharField(max_length=250)
    # use pk value for num added

class Suba(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.CharField(max_length=250)
    vote = models.IntegerField()

class Voted1(models.Model):
    voter = models.ForeignKey('auth.User')
    voted = models.BooleanField(default=False)
