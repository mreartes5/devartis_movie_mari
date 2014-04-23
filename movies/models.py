#! coding: utf-8
from django.db import models
from registration.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100, unique=True)
    year = models.CharField(max_length=50)
    imdb_rank = models.FloatField(default=0)
    imdb_votes = models.IntegerField(default=0)
    current_rating = models.FloatField(default=0)
    total_votes = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)

    def average_rating(self, value):
        self.current_rating = (self.current_rating + float(value)) / 2

    def new_vote(self):
        self.total_votes += 1

    def __unicode__(self):
        return u'Movie [{title}, {year}, {rank}, {votes}]'.format(
            title=self.title,
            year=self.year,
            rank=self.imdb_rank,
            votes=self.imdb_votes)


class Rating(models.Model):
    value = models.IntegerField()
    user = models.ForeignKey(User)
    movie = models.ForeignKey(Movie)


class UserProfile(models.Model):
    user = models.OneToOneField(User)  #(settings.AUTH_USER_MODEL)
    watchlist = models.ManyToManyField(Movie)
