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


def get_cast(id):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/tv/{id}/credits', params=payload).json()
    cast_members = response['cast']
    cast = []
    for person in cast_members:
        cast.append({
            'name': person['name'],
            'id': person['id']
        })
    return cast


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
    genres = ", ".join([genre['name']
                        for genre in response['genres']])
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
        'genres': genres,
        'vote_average': response.get('vote_average', None),
        'added': True,
    }
    return show
