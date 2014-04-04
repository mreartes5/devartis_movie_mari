#! coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg



# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


class Movie(models.Model):
    title = models.CharField(max_length=100, unique=True)
    year = models.CharField(max_length=50)
    imdb_rank = models.FloatField(default=0)
    imdb_votes = models.IntegerField(default=0)

    def average_rating(self):
        #calcular rating en funcion de instancias de Rating asociados
        rating = Rating.objects.filter(movie=self).aggregate(Avg('value'))

        return rating

    # def total_votes(self):
    #     votes = self.imdb_votes +

    def __unicode__(self):
        return u'Movie [{title}, {year}, {rank}, {votes}]'.format(
            title=self.title,
            year=self.year,
            rank=self.imdb_rank,
            votes=self.imdb_votes)


class Rating(models.Model):
    movie = models.ForeignKey(Movie)
    user = models.ForeignKey(UserProfile)
    value = models.IntegerField(default=0)

    def __unicode__(self):
        return u'Rating [{user}, {value},{movie}'.format(
            user=self.user,
            value=self.value,
            movie=self.movie)