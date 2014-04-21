from django.contrib import admin
from registration.models import User
from movies.models import UserProfile
from movies.models import Movie
# from movies.models import MyUser

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Movie)
# admin.site.register(MyUser)