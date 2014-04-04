from django.conf.urls import patterns, url

from movies import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^restricted/', views.restricted, name='restricted'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^movie/(?P<movie_id>\d+)/$', views.movie, name='movie'),
                       url(r'^movie/(?P<movie_id_url>\d+)/add_rating/$', views.add_rating, name='add_rating'),
)