from django.shortcuts import render
from . import people_helper
import json
from django.http import HttpResponse, HttpResponseRedirect
from .models import Person
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_person(request, id):
    person = people_helper.get_person(id)
    movie_credits, tv_credits = people_helper.get_credits(
        id, person['known_for_department'])
    # paginated_credits = Paginator(movie_credits, 10)
    # tv_credits = people_helper.get_tv_credits(
    #     id, person['known_for_department'])

    return render(request, f'people/person.html', {'person': person, 'movie_credits': movie_credits, 'tv_credits': tv_credits})
