from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.http import require_POST

from movies.forms import UserForm, UserProfileForm, SearchForm
from movies.forms import RatingForm, TagForm
from movies.models import Movie, UserProfile, Tag


def index(request):
    context = RequestContext(request)

    movies_list = Movie.objects.order_by('title')
    context_dict = {'boldmessage': "Here are the best movies", 'movies': movies_list}

    # for movie in movies_list:
    #     movie.url = movie.id
    #     #movie.url = movie.title.replace(' ', '_')

    return render_to_response('movies/index.html', context_dict, context)
    #return HttpResponse("Movies Mari")


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
        'movies/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/movies/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your movies account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('movies/login.html', {}, context)


def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are logged in.")
    else:
        return HttpResponse("You are not logged in.")


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see all movies!")


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/movies/')


def movie_show(request, movie_id):
    context = RequestContext(request)

    context_dict = {'movie_id': movie_id, 'tags': Tag.objects.order_by('name')}

    try:
        current_movie = Movie.objects.get(id=movie_id)

        context_dict['movie'] = current_movie
        context_dict['rating_form'] = RatingForm()

    except Movie.DoesNotExist:
        pass

    return render_to_response('movies/movie.html', context_dict, context)


@login_required
def user_watchlist(request, user_id):
    context = RequestContext(request)

    context_dict = {'user_id': user_id}

    try:
        current_user = request.user
        context_dict['user'] = current_user

        watchlist = current_user.watchlist
        context_dict['watchlist'] = watchlist.all().order_by('title')

    except UserProfile.DoesNotExist:
        pass

    return render_to_response('movies/watchlist.html', context_dict, context)


@login_required
def tags_movie_show(request, movie_id):
    context = RequestContext(request)
    context_dict = {'movie_id': movie_id}

    try:
        current_movie = get_object_or_404(Movie, pk=movie_id)
        context_dict['movie'] = current_movie

        current_movie_tags = current_movie.tags.all().order_by('name')
        context_dict['tags'] = current_movie_tags

    except Movie.DoesNotExist:
        pass

    return render_to_response('movies/movieTags.html', context_dict, context)


# @require_POST
# def add_rating_to_movie(request, movie_id):
#     current_movie = get_object_or_404(Movie, pk=movie_id)
#
#     new_value = request.POST['rating']
#
#     current_movie.average_rating(new_value)
#     current_movie.new_vote()
#     current_movie.save()
#
#     return redirect('movies:movie_show', movie_id=movie_id)

@require_POST
def add_rating_to_movie(request, movie_id):
    context = RequestContext(request)

    rating_form = RatingForm(data=request.POST)
    current_movie = get_object_or_404(Movie, pk=movie_id)
    context_dict = {'movie': current_movie}

    if rating_form.is_valid():
        new_value = rating_form.cleaned_data['value']
        current_movie.average_rating(new_value)
        current_movie.new_vote()
        current_movie.save()
        context_dict['rating_form'] = RatingForm()
    else:
        context_dict['rating_form'] = rating_form

    return render_to_response('movies/movie.html', context_dict, context)


def get_or_create_tag(tag_name):

    if len(Tag.objects.filter(name=tag_name)) != 0:
        tag = Tag.objects.get(name=tag_name)

    else:
        tag = Tag(name=tag_name)
        tag.save()

    return tag


@require_POST
def add_tag_to_movie(request, movie_id):
    current_movie = get_object_or_404(Movie, pk=movie_id)

    current_tag_name = request.POST['name']
    tags_name = current_tag_name.split(',')

    for tag_name in tags_name:
        current_tag = get_or_create_tag(tag_name)
        current_movie.tags.add(current_tag)

    return redirect('movies:movie_show', movie_id=movie_id)




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

    movies_to_list = request.user.watchlist
    movies_to_list.add(current_movie)

    return redirect('movies:user_watchlist', user_id=request.user.id)


def search_movies(request):
    context = RequestContext(request)

    context_dict = {}

    if request.method == 'POST':
        search_form = SearchForm(data=request.POST)
        context_dict['search_form'] = search_form

        search_title = request.POST['title']
        search_year_from = request.POST['year_from']
        search_year_to = request.POST['year_to']

        if search_form.is_valid():

            matched_movies = Movie.objects.filter(title__icontains=search_title, year__gte=search_year_from,
                                                  year__lte=search_year_to)

            context_dict['matched_movies'] = matched_movies

        else:
            print search_form.errors

    else:
        search_form = SearchForm()

        context_dict['search_form'] = search_form

    return render_to_response('movies/searchMovies.html', context_dict, context)


"""
def add_tag_to_movie(request, movie_id):
    context = RequestContext(request)
    context_dict = {}

    current_movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'POST':
        tag_form = TagForm(data=request.POST)
        context_dict['tag_form'] = tag_form

        current_tag = request.POST.get('name', False)

        if tag_form.is_valid():

            new_tag = Tag()
            new_tag.name = current_tag
            new_tag.movies.add(current_movie)
            new_tag.save()

        else: 
            print tag_form.errors    

    else:
        tag_form = TagForm()
        context_dict['tag_form'] = tag_form

    #return redirect('movies:movie_show', movie_id=movie_id)
    return render_to_response('movies/movie.html', context_dict, context)
"""

