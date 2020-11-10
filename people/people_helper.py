import requests
import os

movie_api_key = os.getenv("MOVIE_DB_KEY")


def get_person(id):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/person/{id}', params=payload).json()
    if response['profile_path']:
        response['image'] = get_image(response['profile_path'])
    return response


def get_credits(id, known_for):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/person/{id}/combined_credits', params=payload).json()
    if known_for == 'Acting' or response.get('known_for_department') == 'Acting':
        return parse_acting_credits(response['cast'])
    else:
        return parse_crew_credits(response['crew'])


def get_image(profile_path):
    return 'https://image.tmdb.org/t/p/original' + profile_path


def parse_acting_credits(credits):
    movie_credits = []
    tv_credits = []
    for credit in credits:
        if credit['media_type'] == 'movie':
            movie_credits.append({
                'title':  credit.get('title', None),
                'job':  credit.get('character', None),
                'overview':  credit.get('overview', None),
                'release_date': credit.get('release_date', None),
                'vote_average':  credit.get('vote_average', None),
                'movie_id': credit['id'],
                'movie_url': '/films/'+str(credit['id'])+'/view'
            })
        elif credit['media_type'] == 'tv':
            tv_credits.append({
                'name':  credit.get('name', None),
                'job':  credit.get('character', None),
                'overview':  credit.get('overview', None),
                'release_date': credit.get('first_air_date', None),
                'episode_count': credit.get('episode_count', None),
                'vote_average':  credit.get('vote_average', None),
                'show_id': credit.get('id'),
                'show_url': '/shows/'+str(credit['id'])+'/view'
            })
    return movie_credits, tv_credits


def parse_crew_credits(credits):
    movie_credits = []
    tv_credits = []
    for credit in credits:
        if credit['media_type'] == 'movie':
            movie_credits.append({
                'title': credit.get('title', None),
                'job': credit.get('job', None),
                'overview': credit.get('overview', None),
                'release_date': credit.get('release_date', None),
                'vote_average': credit.get('vote_average', None),
                'movie_id': credit['id'],
                'movie_url': '/films/'+str(credit['id'])+'/view'
            })
        elif credit['media_type'] == 'tv':
            tv_credits.append({
                'name': credit.get('name', None),
                'job': credit.get('job', None),
                'overview':  credit.get('overview', None),
                'release_date': credit.get('first_air_date', None),
                'episode_count': credit.get('episode_count', None),
                'vote_average':  credit.get('vote_average', None),
                'show_id': credit.get('id'),
                'show_url': '/shows/'+str(credit['id'])+'/view'
            })
    return movie_credits, tv_credits
