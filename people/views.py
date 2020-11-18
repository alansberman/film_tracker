from django.shortcuts import render
from . import people_helper
import json
from django.http import HttpResponse, HttpResponseRedirect
from .models import Person
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
import requests
from operator import itemgetter


movie_api_key = os.getenv("MOVIE_DB_KEY")


def get_person(request, id):
    person = people_helper.get_person(id)
    movie_credits, tv_credits = people_helper.get_credits(
        id, person['known_for_department'])
    # thanks to https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
    movie_credits = sorted(
        movie_credits, key=itemgetter('vote_average'), reverse=True)
    tv_credits = sorted(
        tv_credits, key=itemgetter('vote_average'), reverse=True)
    movie_paginator = Paginator(movie_credits, 10)
    tv_paginator = Paginator(tv_credits, 10)
    page = request.GET.get('page')
    is_movie = request.GET.get('movie')
    try:
        if is_movie == 'True':
            movie_credits = movie_paginator.page(page)
            tv_credits = tv_paginator.page(1)
        elif is_movie == 'False':
            tv_credits = tv_paginator.page(page)
            movie_credits = movie_paginator.page(1)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        movie_credits = movie_paginator.page(1)
        tv_credits = tv_paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        if is_movie == 'True':
            movie_credits = movie_paginator.page(movie_paginator.num_pages)
        elif is_movie == 'False':
            tv_credits = tv_paginator.page(tv_paginator.num_pages)
    if not page:
        movie_credits = movie_paginator.page(1)
        tv_credits = tv_paginator.page(1)
    return render(request, f'people/person.html', {'person': person, 'movie_credits': movie_credits, 'tv_credits': tv_credits, 'page': page})


def like_person(request, id):
    person = people_helper.get_person_for_create(id)
    liked_person = Person(
        name=person['name'], known_for=person['known_for'], movie_db_id=person['movie_db_id'])
    liked_person.save()
    return HttpResponseRedirect('/people/liked')


def liked_people(request):
    # pylint: disable=no-member
    people = Person.objects.all()
    people_paginator = Paginator(people, 10)
    page = request.GET.get('page')
    try:
        people = people_paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        people = people_paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        people = people_paginator.page(people_paginator.num_pages)
    if not page:
        people = people_paginator.page(1)
    return render(request, 'people/liked.html', {'people': people, 'page': page})


def search(request):
    # if this is a POST request we need to process the form data
    # if request.method == 'POST':
    #     # create a form instance and populate it with data from the request:
    #     form = FilmSearchForm(request.POST)
    #     # check whether it's valid:
    #     if form.is_valid():
    #         # process the data in form.cleaned_data as required
    #         # ...
    #         # redirect to a new URL:
    #         query = form.cleaned_data['search_query']
    #         payload = {
    #             'api_key': 'e6b24f5371e6fd462a8a26499fd466b2', 'query': query}
    #         response = requests.get(
    #             'https://api.themoviedb.org/3/search/multi', params=payload)
    #         films, people = film_helper.parse_search(response.json(), query)
    #         context = {'films': films,
    #                    'query': payload['query'], 'people': people}
    #         return render(request, 'films/search.html', context)

    # if a GET (or any other method) we'll create a blank form
    if request.GET.get('query'):
        query = request.GET.get('query')
        payload = {
            'api_key': movie_api_key, 'query': query}
        response = requests.get(
            'https://api.themoviedb.org/3/search/person', params=payload)
        people = people_helper.parse_search(response.json(), query)

        page = request.GET.get('page')
        people_paginator = Paginator(people, 10)
        try:
            people = people_paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            people = people_paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            people = people_paginator.page(people_paginator.num_pages)
        if not page:
            people = people_paginator.page(1)
        return render(request, 'people/search.html', {'people': people, 'page': page, 'query': query})

    # elif not request.GET.get('page'):
    #     form = FilmSearchForm()

    # return render(request, 'people/search.html', {'form': FilmSearchForm})
