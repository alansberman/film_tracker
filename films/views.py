from django.shortcuts import render, redirect
import requests
from . import film_helper
import json
from datetime import date
import timeit
import functools
import collections
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from imdb import IMDb
from django.db.models.functions import ExtractYear
from .models import Film, Genre, Keyword, CrewCredit, ActingCredit, Token
from .forms import FilmSearchForm, FilmForm
from django.views.decorators.csrf import csrf_exempt

from . import stats
import time
from django.db.models.functions import Trunc
from plotly.offline import plot
from plotly.graph_objs import Scatter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg, Max, Q, Count, FloatField, F, DateField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from datetime import datetime as dt
from django.forms.models import model_to_dict
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# create an instance of the IMDb class

# https://api.themoviedb.org/3/search/movie
import os


movie_api_key = os.getenv("MOVIE_DB_KEY")


def years_chart(request, *filters):
    f = request.GET
    filters = {}
    current_user = request.user
    # print(current_user)
    # print(current_user.id)
    for key, value in f.items():
        if key == 'genre__in':
            value = value.split("&")
            value = [eval(x) for x in value]
            filters[key] = value
        if value == 'True':
            filters[key] = eval(value)
        else:
            filters[key] = value
    wishlist = True if f.get('wishlisted') == 'True' else False
    if 'genre__in' in filters.keys():
        # pylint: disable=no-member
        film_ids = Genre.objects.filter(
            movie_db_id__in=filters['genre__in']).values('film')
        del filters['genre__in']
        filters['pk__in'] = film_ids

    if current_user:
        filters['user'] = current_user

    labels = []
    data = {
        'one': [],
        'two': []
    }

    # pylint: disable=no-member
    films = Film.objects.filter(**filters).annotate(
        year=ExtractYear('release_date')).values('year').annotate(count=Count('year')).annotate(avg_score=Avg('score')) if filters else Film.objects.all().annotate(
        year=ExtractYear('release_date')).values('year').annotate(count=Count('year'))
    for entry in films:
        labels.append(entry['year'])
        data.get('one').append(entry['count'])
        if filters:
            data.get('two').append(entry['avg_score'])
    max_count = max(data.get('one'))
    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'max': max_count
    })


def decades_chart(request, *filters):
    f = request.GET
    filters = {}
    current_user = request.user
    # print(current_user)
    # print(current_user.id)
    for key, value in f.items():
        if key == 'genre__in':
            value = value.split("&")
            value = [eval(x) for x in value]
            filters[key] = value
        if value == 'True':
            filters[key] = eval(value)
        else:
            filters[key] = value
    wishlist = True if f.get('wishlisted') == 'True' else False

    if 'genre__in' in filters.keys():
        # pylint: disable=no-member
        film_ids = Genre.objects.filter(
            movie_db_id__in=filters['genre__in']).values('film')
        del filters['genre__in']
        filters['pk__in'] = film_ids

    if current_user:
        filters['user'] = current_user

    labels = []
    data = {
        'one': [],
        'two': []
    }

    # pylint: disable=no-member
    films = Film.objects.filter(**filters).annotate(
        year=ExtractYear('release_date')) if filters else Film.objects.all().annotate(
        year=ExtractYear('release_date'))

    breakdown = {
        '1930s': (films.filter(year__gte=1930, year__lte=1939).count(), (films.filter(year__gte=1930, year__lte=1939).values_list(
            'score').aggregate(Avg('score'))['score__avg'])),
        '1940s': (films.filter(year__gte=1940, year__lte=1949).count(), (films.filter(year__gte=1940, year__lte=1949).values_list(
            'score').aggregate(Avg('score'))['score__avg'])),
        '1950s': (films.filter(year__gte=1950, year__lte=1959).count(), (films.filter(year__gte=1950, year__lte=1959).values_list(
            'score').aggregate(Avg('score'))['score__avg'])),
        '1960s': (films.filter(year__gte=1960, year__lte=1969).count(), (films.filter(year__gte=1960, year__lte=1969).values_list(
            'score').aggregate(Avg('score'))['score__avg'])),
        '1970s': (films.filter(year__gte=1970, year__lte=1979).count(), (films.filter(year__gte=1970, year__lte=1979).values_list(
            'score').aggregate(Avg('score'))['score__avg'])),
        '1980s': (films.filter(year__gte=1980, year__lte=1989).count(), (films.filter(year__gte=1980, year__lte=1989).values_list(
            'score').aggregate(Avg('score'))['score__avg'])),
        '1990s': (films.filter(year__gte=1990, year__lte=1999).count(), (films.filter(year__gte=1990, year__lte=1999).values_list(
            'score').aggregate(Avg('score'))['score__avg'])),
        '2000s': (films.filter(year__gte=2000, year__lte=2009).count(), (films.filter(year__gte=2000, year__lte=2009).values_list(
            'score').aggregate(Avg('score'))['score__avg'])),
        '2010s': (films.filter(year__gte=2010, year__lte=2019).count(), (films.filter(year__gte=2010, year__lte=2019).values_list(
            'score').aggregate(Avg('score'))['score__avg'])),
    }

    for key, value in breakdown.items():
        labels.append(key)
        data['one'].append(value[0])
        data['two'].append(value[1])
    max_count = max(data.get('one'))

    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'max': max_count
    })


def runtime_chart(request, *filters):
    f = request.GET
    filters = {}
    current_user = request.user
    # print(current_user)
    # print(current_user.id)
    for key, value in f.items():
        if key == 'genre__in':
            value = value.split("&")
            value = [eval(x) for x in value]
            filters[key] = value
        if value == 'True':
            filters[key] = eval(value)
        else:
            filters[key] = value
    wishlist = True if f.get('wishlisted') == 'True' else False

    if 'genre__in' in filters.keys():
        # pylint: disable=no-member
        film_ids = Genre.objects.filter(
            movie_db_id__in=filters['genre__in']).values('film')
        del filters['genre__in']
        filters['pk__in'] = film_ids

    if current_user:
        filters['user'] = current_user

    labels = []
    data = {
        'one': [],
        'two': []
    }
    # pylint: disable=no-member
    films = Film.objects.filter(**filters).values('runtime').annotate(count=Count('runtime')).annotate(avg_score=Avg(
        'score')) if filters else Film.objects.all().values('runtime').annotate(count=Count('runtime')).annotate(avg_score=Avg('score'))
    for entry in films:
        labels.append(entry['runtime'])
        data['one'].append(entry['count'])
        data['two'].append(entry['avg_score'])
    max_count = max(data.get('one'))

    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'max': max_count
    })


def ratings_chart(request, *filters):
    f = request.GET
    filters = {}
    current_user = request.user
    # print(current_user)
    # print(current_user.id)
    for key, value in f.items():
        if key == 'genre__in':
            value = value.split("&")
            value = [eval(x) for x in value]
            filters[key] = value
        if value == 'True':
            filters[key] = eval(value)
        else:
            filters[key] = value
    wishlist = True if f.get('wishlisted') == 'True' else False

    if 'genre__in' in filters.keys():
        # pylint: disable=no-member
        film_ids = Genre.objects.filter(
            movie_db_id__in=filters['genre__in']).values('film')
        del filters['genre__in']
        filters['pk__in'] = film_ids

    if current_user:
        filters['user'] = current_user

    labels = []
    data = {
        'one': [],
        'two': []
    }
    # pylint: disable=no-member
    # pylint: disable=no-member
    films = Film.objects.filter(**filters).values('vote_average').annotate(count=Count('vote_average')) if filters else Film.objects.all(
    ).values('vote_average').annotate(count=Count('vote_average'))

    films_my_score = Film.objects.filter(**filters).values('score').annotate(count_score=Count('score')) if filters else Film.objects.all(
    ).values('score').annotate(count_score=Count('score'))

    d = {}
    for entry in films:
        d[entry['vote_average']] = (entry['count'], 0)
    for entry in films_my_score:
        if d.get(entry['score']) is not None:
            old = d[entry['score']]
            d[entry['score']] = (old[0], entry['count_score'])
        else:
            d[entry['score']] = (0, entry['count_score'])
    d = {k: v for k, v in d.items() if k is not None}
    d = collections.OrderedDict(sorted(d.items()))
    for key, value in d.items():
        labels.append(key)
        data['one'].append(value[0])
        data['two'].append(value[1])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def index(request):
    # print(request.user)
    # # permission_classes = (IsAuthenticated,)
    # # authentication_class = JSONWebTokenAuthentication
    # print(request.user.is_authenticated)

    # film_helper.bulk_create_films(request)

    # pylint: disable=no-member
    if not request.user:
        films = Film.objects.filter(added=True).order_by('-score')
    else:
        films = Film.objects.filter(
            added=True, user=request.user).order_by('-vote_average')
    films = list(films.values())
    # film_paginator = Paginator(films, 10)
    # page = request.GET.get('page')
    # try:
    #     films = film_paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer deliver the first page
    #     films = film_paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range deliver last page of results
    #     films = film_paginator.page(film_paginator.num_pages)
    # if not page:
    #     films = film_paginator.page(1)

    return JsonResponse(data={
        'films': films
    })


def discover(request):
    f = request.GET
    # print(current_user)
    # print(current_user.id)
    filters = {}
    for key, value in f.items():
        if key == 'genre__in':
            value = value.split("&")
            value = ",".join([eval(x) for x in value])
            filters[key] = value
        else:
            filters[key] = value
    filters['sort_by'] = 'vote_count.desc'
    films = film_helper.discover(**filters)
    return JsonResponse(data={'films': films})


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

    # return render(request, f'films/film.html', {'film': film, 'credits': credits, 'cast': cast[:5],
    #                                             'wishlisted': wishlisted, 'watched': watched, 'review': review, 'poster': poster, 'where': where_to_watch})
    return JsonResponse(data={'film': film, 'credits': credits, 'cast': cast[:5],
                              'wishlisted': wishlisted, 'watched': watched, 'review': review, 'poster': poster, 'where': where_to_watch})


def search_results(request):
    return render(request, 'films/search.html', {})


@csrf_exempt
def add_movie(request, movie_id):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        data = json.loads(request.body)
        date_watched = data.get('date_watched')
        score = eval(data.get('score'))
        liked = data.get('liked')
        comments = data.get('comments')
        film, genres, keywords, nb_credits, cast = film_helper.get_film_for_create(
            movie_id)
        film_helper.save_film(film, genres, keywords, nb_credits, cast, wishlisted=False,
                              date_watched=date_watched, score=score, added=True, comments=comments, liked=liked, user=request.user)
        return JsonResponse(data={'response': 'Film successfully added'})

        #     return HttpResponseRedirect('/films')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FilmForm()

    return render(request, 'films/add.html', {'form': form, 'id': movie_id})


def wishlist_movie(request, movie_id):
    if not request.user:
        return JsonResponse(data={'response': 'No user given/found'})
    film, genres, keywords, nb_credits, cast = film_helper.get_film_for_create(
        movie_id)
    # pylint: disable=no-member
    film_found = Film.objects.filter(
        movie_db_id=film['movie_db_id'], user=request.user).exists()
    if film_found:
        return JsonResponse(data={'response': 'Film already wishlisted'})
    try:
        film_helper.save_film(film, genres, keywords, nb_credits,
                              cast, wishlisted=True, user=request.user)
        return JsonResponse(data={'response': 'Film successfully wishlisted'})
    except:
        return JsonResponse(data={'response': 'Failed to wishlist'})


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
        # film_paginator = Paginator(films, 10)
        # page = request.GET.get('page')
        # try:
        #     films = film_paginator.page(page)
        # except PageNotAnInteger:
        #     # If page is not an integer deliver the first page
        #     films = film_paginator.page(1)
        # except EmptyPage:
        #     # If page is out of range deliver last page of results
        #     films = film_paginator.page(film_paginator.num_pages)
        # if not page:
        #     films = film_paginator.page(1)

        return JsonResponse(data={'films': films, 'people': people})
        # return render(request, 'films/search.html', context)

    elif not request.GET.get('page'):
        form = FilmSearchForm()

    return render(request, 'films/search.html', {'form': FilmSearchForm})


def popular(request):
    films = film_helper.get_popular()
    return render(request, 'films/popular.html', {'films': films})


def festivals(request):
    return render(request, 'films/festivals.html')


def genres(request):
    genres = film_helper.get_genres()
    return JsonResponse(data={'genres': genres})


def statistics(request):
    f = request.GET
    filters = {}
    # film_helper.bulk_create_films()
    current_user = request.user
    # print(current_user)
    # print(current_user.id)
    for key, value in f.items():
        if key == 'genre__in':
            value = value.split("&")
            value = [eval(x) for x in value]
            filters[key] = value
        if value == 'True':
            filters[key] = eval(value)
        else:
            filters[key] = value
    wishlist = True if f.get('wishlisted') == 'True' else False

    if current_user:
        filters['user'] = current_user

    if 'genre__in' in filters.keys():
        # pylint: disable=no-member
        film_ids = Genre.objects.filter(
            movie_db_id__in=filters['genre__in']).values('film')
        del filters['genre__in']
        filters['pk__in'] = film_ids
    # pylint: disable=no-member
    films = Film.objects.filter(**filters)
    if films.count() == 0:
        return JsonResponse(data={
            'noFilmsFound': True
        })
    genres = stats.get_genre_percentages(**filters)
    keywords = stats.get_keyword_percentages(**filters)
    liked_percentage = Film.objects.filter(
        **filters).filter(liked=True).count() / Film.objects.filter(**filters).count() * 100
    runtime_breakdowns = list(stats.get_runtime_breakdowns(**filters).values())
    cast = list(ActingCredit.objects.order_by().values(
        'name', 'movie_db_id').annotate(count=Count('id')).order_by('-count').values())
    average_rating = list(stats.get_average_rating(**filters).values())
    average_score = list(stats.get_my_average_score(**filters).values())
    most_recommended = stats.get_most_recommended(**filters)
    nb_credits = stats.get_nb_credit_percentages(**filters)
    cast = stats.get_actor_percentages(**filters)
    decade_breakdown = stats.get_decade_percentages(**filters)
    year_percentages = stats.get_year_percentages(**filters)
    headline = stats.get_headline(**filters)

    statistics = {
        'average_length': films.aggregate(Avg('runtime')),
        'average_crit': Film.objects.filter(critics_pick=True, **filters).count() / Film.objects.filter(**filters).count() * 100,
        'average_rating': average_rating,
        'genres': genres,
        'keywords': keywords,
        # 'credits': credits,
        'cast': cast,
        'num_films': Film.objects.filter(**filters).count(),
        'nb_credits': nb_credits,
        'films': list(films.values()),
        'runtime_breakdown': runtime_breakdowns,
        'most_recommended': most_recommended,
        'year_percentages': year_percentages,
        'average_score': average_score,
        'decade_breakdown': decade_breakdown,
        'liked_percentage': liked_percentage,
        'headline': headline
    }

    return JsonResponse(data={
        'statistics': statistics,
        'wishlist': wishlist
    })
    # return render(request, 'films/statistics.html', {'statistics': statistics, 'filters': filters, 'wishlist': wishlist})


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
