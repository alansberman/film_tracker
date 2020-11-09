import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from os import environ
from dotenv import load_dotenv
load_dotenv()

movie_api_key = environ.get("MOVIE_DB_KEY")


def parse_search(response, query):
    films = []
    people = []
    # credit = requests.get(
    #     f'https://api.themoviedb.org/3/movie/{response["results"][0]["id"]}/credits', params=payload)
    for item in response['results'][:10]:
        if item['media_type'] == 'movie':
            films.append(parse_search_item(item, query))
        elif item['media_type'] == 'person':
            people.append(parse_search_item(item, query))
    # crew_members = credit.json()['crew']
    # for item in crew_members:
    #     if item['job'] == 'Director':
    #         print(item)
    return films, people


def parse_search_item(item, query):
    if item['media_type'] == 'movie':
        if (query.upper() in item['title'].upper()) or (query.upper() in item['original_title']):
            item['genres'] = get_genres(item['id'])
            return item
    elif item['media_type'] == 'person':
        if query.upper() in item['name'].upper():
            if item['known_for'][0]['media_type'] != 'tv':
                person = {
                    'id': item['id'],
                    'name': item['name'],
                    'known_for': item['known_for'][0],
                    'popularity': item['popularity']
                }
                return person


def get_review(title, year):
    payload = {'query': title, 'api-key': 'NrLoKOA38QIjxhhXh0y5tEIZ7jrm4l1q'}
    response = requests.get(
        'https://api.nytimes.com/svc/movies/v2/reviews/search.json', params=payload).json()
    for item in response['results']:
        if item['display_title'].upper() == title.upper():
            if item['publication_date'].split("-")[0] == year:
                return item
    return None


def get_poster(id):
    payload = {'api_key': 'e6b24f5371e6fd462a8a26499fd466b2'}
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}/images', params=payload).json()
    for item in response['posters']:
        return 'https://image.tmdb.org/t/p/original'+item['file_path']
    return None


def get_nb_credits(id):
    payload = {'api_key': 'e6b24f5371e6fd462a8a26499fd466b2'}
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}/credits', params=payload).json()
    crew_members = response['crew']
    producers = []
    screenplay = []
    story = []
    assoc_producer = []
    photog = []
    director = []
    for item in crew_members:
        if item['job'] == 'Director':
            director.append({
                'name': item['name'],
                'id': item['id']})
        if item['job'] == 'Screenplay':
            screenplay.append({
                'name': item['name'],
                'id': item['id']})
        if item['job'] == 'Story':
            story.append({
                'name': item['name'],
                'id': item['id']})
        if item['job'] == 'Producer':
            producers.append({
                'name': item['name'],
                'id': item['id']})
        if item['job'] == 'Associate Producer':
            assoc_producer.append({
                'name': item['name'],
                'id': item['id']})
        if item['job'] == 'Director of Photography':
            photog.append({
                'name': item['name'],
                'id': item['id']})
    return {
        'director': director,
        'producers': producers,
        'screenplay': screenplay,
        'story': story,
        'associate_producer': assoc_producer,
        'director_of_photography': photog
    }


def get_film_details(id):
    payload = {'api_key': 'e6b24f5371e6fd462a8a26499fd466b2'}
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}', params=payload).json()
    response['genres'] = ",".join([genre['name']
                                   for genre in response['genres']])
    return response


def get_similar_films(id):
    payload = {'api_key': 'e6b24f5371e6fd462a8a26499fd466b2'}
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}/similar', params=payload).json()
    similar_films = []
    for film in response['results'][:10]:
        similar_films.append({
            'title': film['title'],
            'id': film['id']
        })
    return similar_films


def get_recommendations(id):
    payload = {'api_key': 'e6b24f5371e6fd462a8a26499fd466b2'}
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}/recommendations', params=payload).json()
    recommended_films = []
    for film in response['results'][:10]:
        recommended_films.append({
            'title': film['title'],
            'id': film['id']
        })
    return recommended_films


def get_film_for_create(id):
    payload = {'api_key': 'e6b24f5371e6fd462a8a26499fd466b2'}
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}', params=payload).json()
    genres = get_genres(id)
    film_object = {
        'title':  response.get('title', None),
        'original_language': response.get('original_language', None),
        'overview': response.get('overview', None),
        'release_date': response.get('release_date', None),
        'popularity': response.get('popularity', None),
        'genres': genres,
        'runtime': response.get('runtime', None),
        'budget': response.get('budget', None),
        'revenue': response.get('revenue', None),
        'vote_average': response.get('vote_average', None),
        'added': True,
        'movie_db_id': response['id']
    }
    return film_object


def get_genres(id):
    payload = {'api_key': 'e6b24f5371e6fd462a8a26499fd466b2'}
    genres = ""
    details = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}', params=payload)
    genre_results = details.json()['genres']
    for genre in genre_results:
        genres += genre['name'] + ", "
    return genres[:-2]
