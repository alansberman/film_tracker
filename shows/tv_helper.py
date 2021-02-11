from .models import Show, Genre, CrewCredit, ActingCredit, Recommendation

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg, Max, Q, Count, FloatField
from django.db.models.functions import ExtractYear

import requests
import os

movie_api_key = os.getenv("MOVIE_DB_KEY")


def parse_search(response, query):
    shows = []
    people = []
    for item in response['results']:
        if item['media_type'] == 'tv':
            shows.append(parse_search_item(item, query))
        elif item['media_type'] == 'person':
            people.append(parse_search_item(item, query))
    return shows, people


def parse_search_item(item, query):
    if item['media_type'] == 'tv':
        if (query.upper() in item['name'].upper()) or (query.upper() in item['original_name']):
            return item
    elif item['media_type'] == 'person':
        if query.upper() in item['name'].upper():
            if item['known_for'][0]['media_type'] == 'tv':
                person = {
                    'id': item['id'],
                    'name': item['name'],
                    'known_for': item['known_for'][0],
                    'popularity': item['popularity']
                }
                return person


def get_provider_image(id):
    return "https://image.tmdb.org/t/p/original"+id


def get_where_to_watch(id):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/tv/{id}/watch/providers', params=payload).json()
    results = {
        'buy': [],
        'watch': []
    }
    # Currently just fetch GB
    if response['results'].get('GB') == None or len(response['results']['GB']) == 0:
        return None
    for key, value in response['results']['GB'].items():
        if key == 'flatrate':
            for option in value:
                results['watch'].append(
                    {option['provider_name']: get_provider_image(option['logo_path'])})
        if key == 'buy':
            for option in value:
                results['buy'].append(
                    {option['provider_name']: get_provider_image(option['logo_path'])})
    return results


def get_genres():
    payload = {'api_key': movie_api_key}
    details = requests.get(
        f'https://api.themoviedb.org/3/genre/tv/list', params=payload)
    genres = details.json()['genres']
    return genres


def get_popular():
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/tv/popular', params=payload).json()['results']
    genres = get_genres()
    for item in response:
        item['genres'] = " | ".join([genre['name']
                                     for genre in genres if genre['id'] in item['genre_ids']])
    return response


def get_cast_and_crew(id):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/tv/{id}/credits', params=payload).json()
    cast_members = response['cast']
    crew_members = response['crew']

    cast = []
    crew = []
    for person in cast_members:
        cast.append({
            'name': person['name'],
            'id': person['id'],
            'character': person['character'],
            'credit_id': person['credit_id']
        })
    for person in crew_members:
        crew.append({
            'name': person['name'],
            'id': person['id'],
            'known_for': person['known_for_department'],
            'credit_id': person['credit_id'],
            'job': person['job']
        })
    return cast, crew


def save_show(show, credits, cast, wishlisted=False, score=None, added=False, comments=None):
    show_to_save = Show(name=show['name'],
                        original_language=show['original_language'],
                        original_name=show['original_name'],
                        overview=show['overview'],
                        popularity=show['popularity'],
                        genres=show['genres'],
                        first_air_date=show['first_air_date'],
                        vote_average=show['vote_average'],
                        added=show['added'],
                        type_of_show=show['type_of_show'],
                        status=show['status'],
                        number_of_episodes=show['number_of_episodes'],
                        number_of_seasons=show['number_of_seasons'],
                        score=score,
                        comments=comments,
                        movie_db_id=show['movie_db_id']
                        )
    show_to_save.save()

    store_recommendations(show['movie_db_id'])

    genre_objects = [Genre(movie_db_id=item['id'], name=item['name'],
                           show=show_to_save) for item in show['genres']]
    # pylint: disable=no-member
    Genre.objects.bulk_create(genre_objects)
    credit_objects = [CrewCredit(movie_db_id=item['id'], name=item['name'], show=show_to_save,
                                 job=item['job'], credit_id=item['credit_id']) for item in credits]
    # pylint: disable=no-member
    CrewCredit.objects.bulk_create(credit_objects)
    acting_objects = [ActingCredit(movie_db_id=item['id'], name=item['name'], show=show_to_save,
                                   role=item['role'], credit_id=item['credit_id']) for item in cast]
    # pylint: disable=no-member
    ActingCredit.objects.bulk_create(acting_objects)


def get_season(show_id, season_number):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/tv/{show_id}/season/{season_number}', params=payload).json()
    return response


def get_episode(show_id, season_number, episode_number):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/tv/{show_id}/season/{season_number}/episode/{episode_number}', params=payload).json()
    return response


def store_recommendations(id):
    recommended = get_recommendations(id)
    # pylint: disable=no-member
    show = Show.objects.get(movie_db_id=id)
    recommendation_objects = [Recommendation(movie_db_id=item['id'], title=item['title'],
                                             show=show) for item in recommended]
    # pylint: disable=no-member
    Recommendation.objects.bulk_create(recommendation_objects)


def get_show_details(id):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/tv/{id}', params=payload).json()
    response['genres'] = ", ".join([genre['name']
                                    for genre in response['genres']])
    return response


def get_recommendations(id):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/tv/{id}/recommendations', params=payload).json()
    recommended_shows = []
    for show in response['results'][:10]:
        recommended_shows.append({
            'name': show['name'],
            'id': show['id']
        })
    return recommended_shows


def get_poster(show):
    if show['backdrop_path']:
        return 'https://image.tmdb.org/t/p/original'+show['backdrop_path']
    return None


def get_show_for_create(id):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/tv/{id}', params=payload).json()
    show = {
        'name':  response.get('name', None),
        'original_language': response.get('original_language', None),
        'original_name': response.get('original_name', None),
        'type_of_show': response.get('type', None),
        'status': response.get('status', None),
        'overview': response.get('overview', None),
        'movie_db_id': response.get('id', None),
        'number_of_seasons': response.get('number_of_seasons', None),
        'number_of_episodes': response.get('number_of_episodes', None),
        'popularity': response.get('popularity', None),
        'genres': response.get('genres', None),
        'first_air_date': response.get('first_air_date', None),
        'vote_average': response.get('vote_average', None),
        'added': True
    }
    return show

    # payload = {'api_key': movie_api_key}
    # response = requests.get(
    #     f'https://api.themoviedb.org/3/movie/{id}', params=payload).json()
    # genres = get_genres_of_film(id)
    # keywords = get_keywords(id)
    # poster = get_poster(id)
    # nb_credits, cast = get_nb_credits(id)
    # review = get_review(response.get('title'),
    #                     response['release_date'].split("-")[0])
    # film_object = {
    #     'title':  response.get('title', None),
    #     'original_language': response.get('original_language', None),
    #     'overview': response.get('overview', None),
    #     'release_date': response.get('release_date', None),
    #     'popularity': response.get('popularity', None),
    #     'runtime': response.get('runtime', None),
    #     'wishlisted': False,
    #     'budget': response.get('budget', None),
    #     'revenue': response.get('revenue', None),
    #     'review_url': review['link']['url'] if review else None,
    #     'critics_pick': review['critics_pick'] if review else None,
    #     'review': review['summary_short'] if review else None,
    #     'vote_average': response.get('vote_average', None),
    #     'added': True,
    #     'poster': poster,
    #     'movie_db_id': response['id'],
    # }
    # return film_object, genres, keywords, nb_credits, cast
