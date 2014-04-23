from django.conf.urls import patterns, url

from movies import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^movie/(?P<movie_id>\d+)/$', views.movie_show, name='movie_show'),
                       url(r'^movie/(?P<movie_id>\d+)/add-rating/$', views.add_or_change_rating_to_movie,
                           name='add_or_change_rating_to_movie'),
                       url(r'^my-watchlist/$', views.user_watchlist, name='user_watchlist'),
                       url(r'^movie/(?P<movie_id>\d+)/add-to-list/$', views.add_movie_to_watchlist,
                           name='add_movie_to_list'),
                       url(r'^movie/(?P<movie_id>\d+)/remove-from-movie/$', views.remove_movie_from_watchlist_from_movie,
                           name='remove_movie_from_movie'),
                       url(r'^movie/(?P<movie_id>\d+)/remove-from-list/$', views.remove_movie_from_watchlist_from_list,
                           name='remove_movie_from_list'),
                       url(r'^search-movies/$', views.search_movies, name='search_movies'),
                       url(r'^movie/(?P<movie_id>\d+)/add-tag/$', views.add_tag_to_movie, name='add_tag_to_movie'),
                       url(r'^movie/(?P<movie_id>\d+)/(?P<tag_id>\d+)/remove-tag/$', views.remove_tag_from_movie,
                           name='remove_tag_from_movie'),
                       url(r'^movie/(?P<movie_id>\d+)/tags/$', views.tags_movie_show, name='tags_movie_show'),
)