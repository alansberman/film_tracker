from django.shortcuts import render, redirect
import requests
from . import film_helper
import json
from datetime import date
import timeit
import functools
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from imdb import IMDb
import re
from .models import Film, Genre, Keyword, CrewCredit, ActingCredit
from .forms import FilmSearchForm, FilmForm
from . import stats
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg, Max, Q, Count, FloatField, F
# create an instance of the IMDb class

# https://api.themoviedb.org/3/search/movie
import os


movie_api_key = os.getenv("MOVIE_DB_KEY")


def index(request):
    # pylint: disable=no-member
    films = Film.objects.filter(added=True).order_by('-score')
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
    credits = film_helper.parse_top_credits(nb_credits)
    # similar = film_helper.get_similar_films(id)
    # film['similar'] = similar
    recommendations = film_helper.get_recommendations(id)

    where_to_watch = film_helper.get_where_to_watch(id)
    # pylint: disable=no-member
    wishlisted = Film.objects.filter(
        wishlisted=True, movie_db_id=film['id']).exists()
    watched = Film.objects.filter(
        added=True, movie_db_id=film['id']).exists()
    film['recommendations'] = recommendations
    film['keywords'] = " | ".join([k['name']
                                   for k in film_helper.get_keywords(id)])
    year = film['release_date'].split("-")[0]
    review = film_helper.get_review(film['title'], year)
    poster = film_helper.get_poster(id)
    return render(request, f'films/film.html', {'film': film, 'credits': credits, 'cast': cast[:5],
                                                'wishlisted': wishlisted, 'watched': watched, 'review': review, 'poster': poster, 'where': where_to_watch})


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
            film, genres, keywords, nb_credits, cast = film_helper.get_film_for_create(
                movie_id)

            added_film = Film(title=film['title'],
                              original_language=film['original_language'],
                              overview=film['overview'],
                              popularity=film['popularity'],
                              #   genres=film['genres'],
                              runtime=film['runtime'],
                              budget=film['budget'],
                              revenue=film['revenue'],
                              vote_average=film['vote_average'],
                              added=film['added'],
                              score=score,
                              comments=comments,
                              date_watched=date_watched,
                              release_date=film['release_date'],
                              movie_db_id=film['movie_db_id'],
                              #   genre_ids=film['genre_ids'],
                              poster=film['poster'],
                              wishlisted=film['wishlisted'],
                              liked=None,
                              #   producer_ids=film['producer_ids'],
                              #   producers=film['producers'],
                              #   cast=film['cast'],
                              #   cast_ids=film['cast_ids'],
                              review=film['review'],
                              review_url=film['review_url'],
                              #   keywords=film['keywords'],
                              #   keyword_ids=film['keyword_ids'],
                              critics_pick=film['critics_pick'],
                              #   director_ids=film['director_ids'],
                              #   director=film['director'],
                              #   assoc_producer_ids=film['assoc_producer_ids'],
                              #   assoc_producers=film['assoc_producer'],
                              #   screenplay_ids=film['screenplay_ids'],
                              #   screenplay=film['screenplay'],
                              #   story_ids=film['story_ids'],
                              #   story=film['story'],
                              #   director_of_photography_ids=film['director_of_photography_ids'],
                              #   director_of_photography=film['director_of_photography']
                              )
            added_film.save()
            return HttpResponseRedirect('/films')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FilmForm()

    return render(request, 'films/add.html', {'form': form, 'id': movie_id})


def wishlist_movie(request, movie_id):

    film, genres, keywords, nb_credits, cast = film_helper.get_film_for_create(
        movie_id)
    # pylint: disable=no-member
    film_found = Film.objects.filter(movie_db_id=film['movie_db_id']).exists()
    if film_found:
        return HttpResponseRedirect('/films/wishlist')

    wishlisted_film = Film(title=film['title'],
                           original_language=film['original_language'],
                           overview=film['overview'],
                           popularity=film['popularity'],
                           runtime=film['runtime'],
                           budget=film['budget'],
                           revenue=film['revenue'],
                           vote_average=film['vote_average'],
                           added=False,
                           score=None,
                           comments=None,
                           date_watched=date.today(),
                           release_date=film['release_date'],
                           movie_db_id=film['movie_db_id'],
                           poster=film['poster'],
                           wishlisted=True,
                           liked=None,
                           review=film['review'],
                           review_url=film['review_url'],
                           critics_pick=film['critics_pick'],
                           )
    wishlisted_film.save()

    film_helper.store_recommendations(film['movie_db_id'])

    genre_objects = [Genre(movie_db_id=item['id'], name=item['name'],
                           film=wishlisted_film) for item in genres]
    # pylint: disable=no-member
    Genre.objects.bulk_create(genre_objects)
    # for item in genres:
    #     genre = Genre(movie_db_id=item['id'],
    #                   name=item['name'], film=wishlisted_film)
    #     genre.save()
    # for item in keywords:
    #     keyword = Keyword(movie_db_id=item['id'],
    #                       name=item['name'], film=wishlisted_film)
    #     keyword.save()
    keyword_objects = [Keyword(
        movie_db_id=item['id'], name=item['name'], film=wishlisted_film) for item in keywords]
    # pylint: disable=no-member
    Keyword.objects.bulk_create(keyword_objects)
    # for item in nb_credits:
    #     credit = CrewCredit(
    #         movie_db_id=item['id'], name=item['name'], film=wishlisted_film, job=item['job'], credit_id=item['credit_id'])
    #     credit.save()
    credit_objects = [CrewCredit(movie_db_id=item['id'], name=item['name'], film=wishlisted_film,
                                 job=item['job'], credit_id=item['credit_id']) for item in nb_credits]
    # pylint: disable=no-member
    CrewCredit.objects.bulk_create(credit_objects)
    # for item in cast:
    #     credit = ActingCredit(
    #         movie_db_id=item['id'], name=item['name'], film=wishlisted_film, role=item['role'], credit_id=item['credit_id'])
    #     credit.save()
    acting_objects = [ActingCredit(movie_db_id=item['id'], name=item['name'], film=wishlisted_film,
                                   role=item['role'], credit_id=item['credit_id']) for item in cast]
    # pylint: disable=no-member
    ActingCredit.objects.bulk_create(acting_objects)
    return HttpResponseRedirect('/films/wishlist')


def wishlist(request):
    # pylint: disable=no-member
    films = Film.objects.filter(wishlisted=True).order_by('-score')
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


def festivals(request):
    return render(request, 'films/festivals.html')


def statistics(request):
    # pylint: disable=no-member
    films = Film.objects.filter(wishlisted=True)
    genres = stats.get_genre_percentages()
    keywords = stats.get_keyword_percentages()
    runtime_breakdowns = stats.get_runtime_breakdowns()
    cast = ActingCredit.objects.order_by().values(
        'name', 'movie_db_id').annotate(count=Count('id')).order_by('-count')
    average_rating = stats.get_average_rating()
    most_recommended = stats.get_most_recommended()
    nb_credits = stats.get_nb_credit_percentages()
    cast = stats.get_actor_percentages()
    decade_breakdown = stats.get_decade_percentages()
    year_percentages = stats.get_year_percentages()
    headline = stats.get_headline()
    statistics = {
        'average_length': films.aggregate(Avg('runtime')),
        'average_crit': len(Film.objects.filter(critics_pick=True)) / len(Film.objects.all()) * 100,
        'average_rating': average_rating,
        'genres': genres,
        'keywords': keywords,
        'credits': credits,
        'cast': cast,
        'num_films': len(Film.objects.all()),
        'nb_credits': nb_credits,
        'runtime_breakdown': runtime_breakdowns,
        'most_recommended': most_recommended,
        'year_percentages': year_percentages,
        'decade_breakdown': decade_breakdown,
        'headline': headline
    }
    return render(request, 'films/statistics.html', {'statistics': statistics})


def top(request):
    films = film_helper.get_top_rated()
    return render(request, 'films/top.html', {'films': films})


def upcoming(request):
    films = film_helper.get_upcoming_films()
    return render(request, 'films/upcoming.html', {'films': films})


def like(request, id):
    # pylint: disable=no-member
    film = Film.objects.filter(movie_db_id=id)
    film.update(liked=True)
    for item in film:
        item.save()
    return redirect(request.META['HTTP_REFERER'])


def dislike(request, id):
    # pylint: disable=no-member
    film = Film.objects.filter(movie_db_id=id)
    film.update(liked=False)
    for item in film:
        item.save()
    return redirect(request.META['HTTP_REFERER'])
