#! coding: utf-8
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# from django.db.models import Avg


# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=100, unique=True)
    year = models.CharField(max_length=50)
    imdb_rank = models.FloatField(default=0)
    imdb_votes = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    total_votes = models.IntegerField(default=0)

    def average_rating(self, value):
        self.rating = (self.rating + float(value)) / 2

    # def average_rating(self):
    #     #calcular rating en funcion de instancias de Rating asociados
    #     rating = Rating.objects.filter(movie=self).aggregate(Avg('value'))
    #
    #     return rating

    def new_vote(self):
        self.total_votes += 1

    def __unicode__(self):
        return u'Movie [{title}, {year}, {rank}, {votes}]'.format(
            title=self.title,
            year=self.year,
            rank=self.imdb_rank,
            votes=self.imdb_votes)


# class Watchlist(models.Model):
#     movies = models.ForeignKey(Movie)
#
#     def __unicode__(self):
#         return self.movies

class MyUser(AbstractUser):
    watchlist = models.ManyToManyField(Movie)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.usernamdele

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    movies = models.ManyToManyField(Movie)

    def __unicode__(self):
        return self.name
        
