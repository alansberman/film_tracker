import requests
import os

movie_api_key = os.getenv("MOVIE_DB_KEY")


def get_person(id):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/person/{id}', params=payload).json()
    return response


def get_movie_credits(id, known_for):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/person/{id}/movie_credits', params=payload).json()
    if known_for == 'Acting' or response['known_for_department'] == 'Acting':
        return parse_acting_credits(response['cast'])
    else:
        return parse_crew_credits(response['crew'])


def parse_acting_credits(credits):
    parsed_credits = []
    for credit in credits:
        parsed_credits.append({
            'title':  credit.get('title', None),
            'job':  credit.get('character', None),
            'overview':  credit.get('overview', None),
            'release_date': credit.get('release_date', None),
            'vote_average':  credit.get('vote_average', None),
            'movie_id': credit['id'],
            'movie_url': '/films/'+str(credit['id'])+'/view'
        })
    return parsed_credits


def parse_crew_credits(credits):
    parsed_credits = []
    for credit in credits:
        parsed_credits.append({
            'title': credit.get('title', None),
            'job': credit.get('job', None),
            'overview': credit.get('overview', None),
            'release_date': credit.get('release_date', None),
            'vote_average': credit.get('vote_average', None),
            'movie_id': credit['id'],
            'movie_url': '/films/'+str(credit['id'])+'/view'
        })
    return parsed_credits
