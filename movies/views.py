from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db import models
from django.contrib.auth.models import User

from movies.forms import UserForm, UserProfileForm
from movies.forms import RatingForm, UserWatchlistForm
from movies.models import Movie, UserProfile, MyUser
from django.db.models import Avg


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

@login_required
def user_watchlist(request, user_id):
    context = RequestContext(request)

    context_dict = {'user_id': user_id}

    try:
        user = UserProfile.objects.get(id=user_id)
        context_dict['user'] = user

        watchlist = user.watchlist.order_by('title')
        context_dict['watchlist'] = watchlist

    except UserProfile.DoesNotExist:
        pass

    return render_to_response('movies/watchlist.html', context_dict, context)


def add_rating_to_movie(request, movie_id):
    context = RequestContext(request)
    #movie_title = movie_title_url.replace('_', ' ')

    #context_dict = {'movie_title': movie_title}
    context_dict = {'movie_id': movie_id}

    try:
        current_movie = Movie.objects.get(id=movie_id)

        context_dict['movie'] = current_movie

        if request.method == 'POST':
            new_value = request.POST['rating']
            context_dict['rating'] = new_value

            current_movie.average_rating(new_value)
            current_movie.new_vote()
            current_movie.save()

        else:  # If the request was not a POST, display the form to enter details.
            rating_form = RatingForm()

            context_dict['rating'] = rating_form

    except Movie.DoesNotExist:
        pass

    return render_to_response('movies/movie.html', context_dict, context)


def add_movie_to_watchlist(request, movie_id):
    context = RequestContext(request)
    #movie_title = movie_title_url.replace('_', ' ')

    #context_dict = {'movie_title': movie_title}
    context_dict = {'movie_id': movie_id}

    try:
        current_movie = Movie.objects.get(id=movie_id)

        context_dict['movie'] = current_movie

        if request.method == 'POST':
            add_movie = UserWatchlistForm(data=request.POST)

            current_user = request.user
            context_dict['user'] = current_user

            current_user_watchlist = current_user.watchlist
            print current_user_watchlist
            context_dict['watchlist'] = current_user_watchlist
            current_user_watchlist.add(add_movie)

            # return HttpResponseRedirect('/movies/')
        else:  # If the request was not a POST, display the form to enter details.
            watchlist_form = UserWatchlistForm()

            context_dict['watchlist'] = watchlist_form

    except Movie.DoesNotExist:
        pass

    return render_to_response('movies/watchlist.html', context_dict, context)