from movies.models import *
from django.db.models import Avg

r = Rating.objects.all()

Rating.objects.filter(movie=Movie.objects.all()[0]).aggregate(Avg('value'))
print Rating.objects.all()