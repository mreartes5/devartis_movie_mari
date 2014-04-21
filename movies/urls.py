from django.conf.urls import patterns, url

from movies import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       # url(r'^register/$', views.register, name='register'),
                       # url(r'^login/$', views.user_login, name='login'),
                       # url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^movie/(?P<movie_id>\d+)/$', views.movie_show, name='movie_show'),
                       url(r'^movie/(?P<movie_id>\d+)/addRating/$', views.add_or_change_rating_to_movie,
                           name='add_or_change_rating_to_movie'),
                       url(r'^mywatchlist/$', views.user_watchlist, name='user_watchlist'),
                       url(r'^movie/(?P<movie_id>\d+)/addtolist/$', views.add_movie_to_watchlist,
                           name='add_movie_to_list'),
                       url(r'^movie/(?P<movie_id>\d+)/removefrommovie/$', views.remove_movie_from_watchlist_from_movie,
                           name='remove_movie_from_movie'),
                       url(r'^movie/(?P<movie_id>\d+)/removefromlist/$', views.remove_movie_from_watchlist_from_list,
                           name='remove_movie_from_list'),
                       url(r'^searchMovies/$', views.search_movies, name='search_movies'),
                       url(r'^movie/(?P<movie_id>\d+)/addTag/$', views.add_tag_to_movie, name='add_tag_to_movie'),
                       url(r'^movie/(?P<movie_id>\d+)/(?P<tag_id>\d+)/removeTag/$', views.remove_tag_from_movie,
                           name='remove_tag_from_movie'),
                       url(r'^movie/(?P<movie_id>\d+)/tags/$', views.tags_movie_show, name='tags_movie_show'),
)