from django.shortcuts import render
from . import tv_helper
from .models import Show
import requests
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ShowSearchForm, ShowForm

# Create your views here.


def index(request):
    # pylint: disable=no-member
    context = {'shows': Show.objects.filter(added=True)}
    return render(request, 'shows/index.html', context)


def search_results(request):
    return render(request, 'tv/search.html', {})


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
                'api_key': 'e6b24f5371e6fd462a8a26499fd466b2', 'query': query}
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
            'api_key': 'e6b24f5371e6fd462a8a26499fd466b2', 'query': query}
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
    context = {'films': Show.objects.filter(wishlisted=True)}
    return render(request, 'shows/wishlist.html', context)


def wishlist_show(request, movie_id):
    return None
    # film = film_helper.get_film_for_create(movie_id)

    # wishlisted_film = Film(title=film['title'],
    #                     original_language=film['original_language'],
    #                     overview=film['overview'],
    #                     popularity=film['popularity'],
    #                     genres=film['genres'],
    #                     runtime=film['runtime'],
    #                     budget=film['budget'],
    #                     revenue=film['revenue'],
    #                     vote_average=film['vote_average'],
    #                     wishlisted=True,
    #                     date_watched=date.today(),
    #                     added=False,
    #                     release_date=film['release_date'],
    #                     movie_db_id=film['movie_db_id']
    #                     )
    # wishlisted_film.save()
    # return HttpResponseRedirect('/films/wishlist')
