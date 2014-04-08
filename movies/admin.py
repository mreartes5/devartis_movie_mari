from django.contrib import admin
from movies.models import UserProfile
from movies.models import Movie, MyUser

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Movie)
admin.site.register(MyUser)