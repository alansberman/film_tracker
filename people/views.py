from django.shortcuts import render
from . import people_helper
import json
from django.http import HttpResponse, HttpResponseRedirect
from .models import Person
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_person(request, id):
    person = people_helper.get_person(id)
    movie_credits = people_helper.get_movie_credits(
        id, person['known_for_department'])
    # paginated_credits = Paginator(movie_credits, 10)

    # try:
    #     page = int(request.GET.get('page'))
    #     paginated_credits = paginated_credits.page(
    #         movie_credits[page*10:(page*10)+10])
    # except PageNotAnInteger:
    #     paginated_credits = paginated_credits.page(1)
    # except EmptyPage:
    #     paginated_credits = paginated_credits.page(paginated_credits.num_pages)
    # except TypeError:
    #     paginated_credits = paginated_credits.page(1)

    return render(request, f'people/person.html', {'person': person, 'movie_credits': movie_credits})
