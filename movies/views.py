from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from registration.models import User

from movies.forms import SearchForm
from movies.forms import RatingForm, TagForm
from movies.models import Movie, Tag, Rating, UserProfile


def index(request):
    context_dict = {'search_form': SearchForm()}

    return render(request, 'movies/index.html', context_dict)


@receiver(post_save, sender=User)
def create_user_profile(sender, created, **kwargs):
    if created:
        current_user = kwargs.get('instance')
        UserProfile.objects.create(user=current_user)


def movie_show(request, movie_id):
    context_dict = {'movie_id': movie_id, 'tags': Tag.objects.order_by('name')}

    try:
        current_movie = Movie.objects.get(id=movie_id)
        context_dict['movie'] = current_movie
        context_dict['movies'] = Movie.objects.all()

        current_user = request.user
        if current_user.is_authenticated():
            context_dict['user_watchlist'] = current_user.userprofile.watchlist.all()

            if current_user.rating_set.filter(movie=current_movie).exists():
                current_movie_voted = True
                context_dict['user_rating_for_movie'] = current_user.rating_set.get(movie=current_movie).value
            else:
                current_movie_voted = False

            context_dict['current_movie_voted'] = current_movie_voted

            context_dict['rating_form'] = RatingForm()
            context_dict['tag_form'] = TagForm()

    except Movie.DoesNotExist:
        context_dict['error'] = 'The movie is not found'

    return render(request, 'movies/movie.html', context_dict)


@login_required
def user_watchlist(request):
    context_dict = {}

    current_user = request.user
    context_dict['user'] = current_user

    user_profile = current_user.userprofile
    #UserProfile.objects.get(user=current_user)
    watchlist = user_profile.watchlist
    context_dict['watchlist'] = watchlist.order_by('title')

    return render(request, 'movies/watchlist.html', context_dict)


def tags_movie_show(request, movie_id):
    context_dict = {'movie_id': movie_id}

    current_movie = get_object_or_404(Movie, pk=movie_id)
    context_dict['movie'] = current_movie
    context_dict['movies'] = Movie.objects.all()

    current_movie_tags = current_movie.tags.all().order_by('name')
    context_dict['tags'] = current_movie_tags

    return render(request, 'movies/movie_tags.html', context_dict)


def update_current_rating_and_total_votes_for_current_movie(current_movie, new_value):
    current_movie.average_rating(new_value)
    current_movie.new_vote()
    current_movie.save()


def change_or_create_user_rating_for_current_movie(current_movie, current_user, new_value):
    if current_user.rating_set.filter(movie=current_movie).exists():
        rating = current_user.rating_set.get(movie=current_movie)
        rating.value = new_value

    else:
        rating = Rating(value=new_value)
        rating.user = current_user
        rating.movie = current_movie

    rating.save()


@require_POST
def add_or_change_rating_to_movie(request, movie_id):
    rating_form = RatingForm(data=request.POST)
    current_movie = get_object_or_404(Movie, pk=movie_id)
    current_user = request.user
    context_dict = {'movie': current_movie, 'movies': Movie.objects.all(), 'tag_form': TagForm(), 'user': current_user}

    if rating_form.is_valid():
        new_value = rating_form.cleaned_data['value']
        update_current_rating_and_total_votes_for_current_movie(current_movie, new_value)
        change_or_create_user_rating_for_current_movie(current_movie, current_user, new_value)

        context_dict['rating_form'] = RatingForm()
        return redirect('movies:movie_show', movie_id=movie_id)

    else:
        context_dict['rating_form'] = rating_form

    return render(request, 'movies/movie.html', context_dict)


def get_or_create_tag(tag_name):
    if Tag.objects.filter(name=tag_name).exists():
        tag = Tag.objects.get(name=tag_name)

    else:
        tag = Tag(name=tag_name)
        tag.save()

    return tag


@require_POST
def add_tag_to_movie(request, movie_id):
    tag_form = TagForm(data=request.POST)
    current_movie = get_object_or_404(Movie, pk=movie_id)
    context_dict = {'movie': current_movie, 'movies': Movie.objects.all(), 'rating_form': RatingForm()}

    if tag_form.is_valid():
        current_tag_name = tag_form.cleaned_data['name']

        tags_name = current_tag_name.split(',')

        for tag_name in tags_name:
            current_tag = get_or_create_tag(tag_name)
            current_movie.tags.add(current_tag)
            context_dict['tag_form'] = TagForm()

        return redirect('movies:movie_show', movie_id=movie_id)

    else:
        context_dict['tag_form'] = tag_form

    return render(request, 'movies/movie.html', context_dict)


@require_POST
def remove_tag_from_movie(request, movie_id, tag_id):
    current_movie = get_object_or_404(Movie, pk=movie_id)

    current_tag = get_object_or_404(Tag, pk=tag_id)

    current_movie_tags = current_movie.tags
    current_movie_tags.remove(current_tag)

    return redirect('movies:tags_movie_show', movie_id=movie_id)


@require_POST
def add_movie_to_watchlist(request, movie_id):
    current_movie = get_object_or_404(Movie, pk=movie_id)

    movies_to_list = request.user.userprofile.watchlist
    movies_to_list.add(current_movie)

    return redirect('movies:movie_show', movie_id=movie_id)


@require_POST
def remove_movie_from_watchlist_from_movie(request, movie_id):
    current_movie = get_object_or_404(Movie, pk=movie_id)

    movies_to_list = request.user.userprofile.watchlist
    movies_to_list.remove(current_movie)

    return redirect('movies:movie_show', movie_id=movie_id)


@require_POST
def remove_movie_from_watchlist_from_list(request, movie_id):
    current_movie = get_object_or_404(Movie, pk=movie_id)

    movies_to_list = request.user.userprofile.watchlist
    movies_to_list.remove(current_movie)

    return redirect('movies:user_watchlist')


def search_filter(search_title, search_year_from, search_year_to):
    matched_movies = Movie.objects.filter(title__icontains=search_title)

    if search_year_from:
        matched_movies = matched_movies.filter(year__gte=search_year_from)

    if search_year_to:
        matched_movies = matched_movies.filter(year__lte=search_year_to)

    return matched_movies


@require_http_methods(["GET", "POST"])
def search_movies(request):
    context_dict = {}

    search_form = SearchForm(data=request.POST)

    if search_form.is_valid():
        search_title = search_form.cleaned_data['title'].strip()
        search_year_from = search_form.cleaned_data['year_from']
        search_year_to = search_form.cleaned_data['year_to']

        matched_movies = search_filter(search_title, search_year_from, search_year_to)

        context_dict['search_form'] = SearchForm()
        context_dict['matched_movies'] = matched_movies

    else:
        context_dict['search_form'] = search_form

    return render(request, 'movies/index.html', context_dict)