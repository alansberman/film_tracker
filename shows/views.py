from django.shortcuts import render
from django.urls import reverse

from . import tv_helper
from .models import Show
import requests
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ShowSearchForm, ShowForm
import os

movie_api_key = os.getenv("MOVIE_DB_KEY")
# Create your views here.


def index(request):
    # pylint: disable=no-member
    context = {'shows': Show.objects.filter(added=True)}
    return render(request, 'shows/index.html', context)


def search_results(request):
    return render(request, 'tv/search.html', {})


def add_show(request, show_id):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ShowForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            score = form.cleaned_data['score']
            comments = form.cleaned_data['comments']
            date_watched = form.cleaned_data['date_watched']

            show = tv_helper.get_show_for_create(show_id)
            added_show = Show(name=show['name'],
                              original_language=show['original_language'],
                              original_name=show['original_name'],
                              overview=show['overview'],
                              popularity=show['popularity'],
                              genres=show['genres'],
                              vote_average=show['vote_average'],
                              added=show['added'],
                              type_of_show=show['type_of_show'],
                              status=show['status'],
                              number_of_episodes=show['number_of_episodes'],
                              number_of_seasons=show['number_of_seasons'],
                              score=score,
                              comments=comments,
                              date_watched=date_watched,
                              movie_db_id=show['movie_db_id']
                              )
            added_show.save()
            return HttpResponseRedirect(reverse('shows:view', args=(show['movie_db_id'],)))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ShowForm()

    return render(request, 'shows/add.html', {'form': form, 'id': show_id})


def get_season(request, id, season_number):
    season = tv_helper.get_season(id, season_number)
    show = tv_helper.get_show_details(id)
    return render(request, f'shows/season.html', {'show': show, 'season': season})


def get_episode(request, id, season_number, episode_number):
    season = tv_helper.get_season(id, season_number)
    show = tv_helper.get_show_details(id)
    episode = tv_helper.get_episode(id, season_number, episode_number)
    return render(request, f'shows/episode.html', {'show': show, 'season': season, 'episode': episode})


def get_show(request, id):
    cast = tv_helper.get_cast(id)
    show = tv_helper.get_show_details(id)
    recommendations = tv_helper.get_recommendations(id)
    # pylint: disable=no-member
    wishlisted = Show.objects.filter(
        wishlisted=True, movie_db_id=show['id']).exists()
    watched = Show.objects.filter(
        added=True, movie_db_id=show['id']).exists()
    show['recommendations'] = recommendations
    poster = tv_helper.get_poster(show)
    return render(request, f'shows/show.html', {'show': show, 'cast': cast, 'wishlisted': wishlisted, 'watched': watched, 'poster': poster})


def search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ShowSearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            query = form.cleaned_data['search_query']
            payload = {
                'api_key': movie_api_key, 'query': query}
            response = requests.get(
                'https://api.themoviedb.org/3/search/multi', params=payload)
            shows, people = tv_helper.parse_search(response.json(), query)
            context = {'shows': shows,
                       'query': payload['query'], 'people': people}
            return render(request, 'shows/search.html', context)

    # if a GET (or any other method) we'll create a blank form
    elif request.GET.get('query'):
        query = request.GET.get('query')
        payload = {
            'api_key': movie_api_key, 'query': query}
        response = requests.get(
            'https://api.themoviedb.org/3/search/multi', params=payload)
        shows, people = tv_helper.parse_search(response.json(), query)
        context = {'shows': shows, 'query': payload['query'], 'people': people}
        return render(request, 'shows/search.html', context)

    else:
        form = ShowSearchForm()

    return render(request, 'shows/search.html', {'form': ShowSearchForm})


def wishlist(request):
    # pylint: disable=no-member
    context = {'shows': Show.objects.filter(wishlisted=True)}
    return render(request, 'shows/wishlist.html', context)


def wishlist_show(request, show_id):
    show = tv_helper.get_show_for_create(show_id)
    wishlisted_show = Show(name=show['name'],
                           original_language=show['original_language'],
                           original_name=show['original_name'],
                           overview=show['overview'],
                           popularity=show['popularity'],
                           genres=show['genres'],
                           vote_average=show['vote_average'],
                           added=False,
                           type_of_show=show['type_of_show'],
                           status=show['status'],
                           number_of_episodes=show['number_of_episodes'],
                           number_of_seasons=show['number_of_seasons'],
                           score=None,
                           comments=None,
                           date_watched=None,
                           wishlisted=True,
                           movie_db_id=show['movie_db_id']
                           )
    wishlisted_show.save()
    return HttpResponseRedirect(reverse('shows:view', args=(show['movie_db_id'],)))


def popular(request):
    shows = tv_helper.get_popular()
    return render(request, 'shows/popular.html', {'shows': shows})
