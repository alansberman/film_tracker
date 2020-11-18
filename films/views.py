from django.shortcuts import render
import requests
from . import film_helper
import json
from datetime import date

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from imdb import IMDb
from .models import Film
from .forms import FilmSearchForm, FilmForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# create an instance of the IMDb class

# https://api.themoviedb.org/3/search/movie
import os


movie_api_key = os.getenv("MOVIE_DB_KEY")


def index(request):
    # pylint: disable=no-member
    films = Film.objects.filter(added=True)
    film_paginator = Paginator(films, 10)
    page = request.GET.get('page')
    try:
        films = film_paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        films = film_paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        films = film_paginator.page(film_paginator.num_pages)
    if not page:
        films = film_paginator.page(1)
    return render(request, 'films/index.html', {'films': films})


def get_film(request, id):
    nb_credits, cast = film_helper.get_nb_credits(id)
    film = film_helper.get_film_details(id)
    # similar = film_helper.get_similar_films(id)
    # film['similar'] = similar
    recommendations = film_helper.get_recommendations(id)
    # pylint: disable=no-member
    wishlisted = Film.objects.filter(
        wishlisted=True, movie_db_id=film['id']).exists()
    watched = Film.objects.filter(
        added=True, movie_db_id=film['id']).exists()
    film['recommendations'] = recommendations
    year = film['release_date'].split("-")[0]
    review = film_helper.get_review(film['title'], year)
    poster = film_helper.get_poster(id)
    return render(request, f'films/film.html', {'film': film, 'credits': nb_credits, 'cast': cast,
                                                'wishlisted': wishlisted, 'watched': watched, 'review': review, 'poster': poster})


def search_results(request):
    return render(request, 'films/search.html', {})


def add_movie(request, movie_id):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FilmForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            score = form.cleaned_data['score']
            comments = form.cleaned_data['comments']
            date_watched = form.cleaned_data['date_watched']

            film = film_helper.get_film_for_create(movie_id)
            added_film = Film(title=film['title'],
                              original_language=film['original_language'],
                              overview=film['overview'],
                              popularity=film['popularity'],
                              genres=film['genres'],
                              runtime=film['runtime'],
                              budget=film['budget'],
                              revenue=film['revenue'],
                              vote_average=film['vote_average'],
                              added=film['added'],
                              score=score,
                              comments=comments,
                              date_watched=date_watched,
                              release_date=film['release_date'],
                              movie_db_id=film['movie_db_id']
                              )
            added_film.save()
            return HttpResponseRedirect('/films')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FilmForm()

    return render(request, 'films/add.html', {'form': form, 'id': movie_id})


def wishlist_movie(request, movie_id):
    film = film_helper.get_film_for_create(movie_id)

    wishlisted_film = Film(title=film['title'],
                           original_language=film['original_language'],
                           overview=film['overview'],
                           popularity=film['popularity'],
                           genres=film['genres'],
                           runtime=film['runtime'],
                           budget=film['budget'],
                           revenue=film['revenue'],
                           vote_average=film['vote_average'],
                           wishlisted=True,
                           date_watched=date.today(),
                           added=False,
                           release_date=film['release_date'],
                           movie_db_id=film['movie_db_id']
                           )
    wishlisted_film.save()
    return HttpResponseRedirect('/films/wishlist')


def wishlist(request):
    # pylint: disable=no-member
    films = Film.objects.filter(wishlisted=True)
    film_paginator = Paginator(films, 10)
    page = request.GET.get('page')
    try:
        films = film_paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        films = film_paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        films = film_paginator.page(film_paginator.num_pages)
    if not page:
        films = film_paginator.page(1)
    return render(request, 'films/wishlist_index.html', {'films': films})


def search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FilmSearchForm(request.POST)
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
            films, people = film_helper.parse_search(response.json(), query)
            context = {'films': films,
                       'query': payload['query'], 'people': people}
            return render(request, 'films/search.html', context)

    # if a GET (or any other method) we'll create a blank form
    elif request.GET.get('query'):
        query = request.GET.get('query')
        payload = {
            'api_key': movie_api_key, 'query': query}
        response = requests.get(
            'https://api.themoviedb.org/3/search/multi', params=payload)
        films, people = film_helper.parse_search(response.json(), query)

        film_paginator = Paginator(films, 10)
        page = request.GET.get('page')
        try:
            films = film_paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            films = film_paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            films = film_paginator.page(film_paginator.num_pages)
        if not page:
            films = film_paginator.page(1)

        context = {'films': films,
                   'query': payload['query'], 'people': people, 'page': page}
        return render(request, 'films/search.html', context)

    elif not request.GET.get('page'):
        form = FilmSearchForm()

    return render(request, 'films/search.html', {'form': FilmSearchForm})


def popular(request):
    films = film_helper.get_popular()
    return render(request, 'films/popular.html', {'films': films})


def top(request):
    films = film_helper.get_top_rated()
    return render(request, 'films/top.html', {'films': films})


def upcoming(request):
    films = film_helper.get_upcoming_films()
    return render(request, 'films/upcoming.html', {'films': films})
