from .models import Film, Recommendation
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import os


movie_api_key = os.getenv("MOVIE_DB_KEY")
nyt_api_key = os.getenv("NYT_KEY")


def parse_search(response, query):
    films = []
    people = []
    # credit = requests.get(
    #     f'https://api.themoviedb.org/3/movie/{response["results"][0]["id"]}/credits', params=payload)
    for item in response['results']:
        if item['media_type'] == 'movie':
            films.append(parse_search_item(item, query))
        elif item['media_type'] == 'person':
            people.append(parse_search_item(item, query))
    # crew_members = credit.json()['crew']
    # for item in crew_members:
    #     if item['job'] == 'Director':
    #         print(item)
    return films, people


def get_keywords(id):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}/keywords', params=payload).json()
    keywords = [keyword for keyword in response['keywords']]
    return keywords


def parse_top_credits(credits):
    top_credits = {
        'directors': [item for item in credits if item['job'] == 'Director'],
        'producers': [item for item in credits if item['job'] == 'Producer'],
        'screenwriters': [item for item in credits if item['job'] == 'Screenplay'],
        'story': [item for item in credits if item['job'] == 'Story'],
        'editors': [item for item in credits if item['job'] == 'Editor'],
        'composers': [item for item in credits if item['job'] == 'Original Music Composer'],
        'photographers': [item for item in credits if item['job'] == 'Director of Photography']
    }
    return top_credits


def parse_search_item(item, query):
    if item['media_type'] == 'movie':
        if (query.upper() in item['title'].upper()) or (query.upper() in item['original_title']):
            item['genres'] = get_genres_of_film(item['id'])
            return item
    elif item['media_type'] == 'person':
        if query.upper() in item['name'].upper():
            if item['known_for']:
                if item['known_for'][0]['media_type'] != 'tv':
                    person = {
                        'id': item['id'],
                        'name': item['name'],
                        'known_for': item['known_for'][0],
                        'popularity': item['popularity']
                    }
                    return person


def get_review(title, year):
    payload = {'query': title, 'api-key': nyt_api_key}
    response = requests.get(
        'https://api.nytimes.com/svc/movies/v2/reviews/search.json', params=payload).json()
    for item in response['results']:
        if item['display_title'].upper() == title.upper():
            if item['publication_date'].split("-")[0] == year:
                return item
    return None


def get_provider_image(id):
    return "https://image.tmdb.org/t/p/original"+id


def get_poster(id):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}/images', params=payload).json()
    for item in response['posters']:
        return 'https://image.tmdb.org/t/p/original'+item['file_path']
    return None


def get_nb_credits(id):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}/credits', params=payload).json()
    cast_members = response['cast']
    cast = []
    for member in cast_members:
        cast.append({
            'name': member['name'],
            'id': member['id'],
            'role': member['character'],
            'credit_id': member['credit_id']
        })
    crew_members = response['crew']
    nb_credits = []
    for item in crew_members:
        nb_credits.append({
            'name': item['name'],
            'id': item['id'],
            'job': item['job'],
            'credit_id': item['credit_id']
        })
    return nb_credits, cast


def get_film_details(id):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}', params=payload).json()
    response['genres'] = " | ".join([genre['name']
                                     for genre in response['genres']])
    return response


def get_similar_films(id):
    payload = {'api_key': movie_api_key}
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
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}/recommendations', params=payload).json()
    recommended_films = []
    for film in response['results'][:10]:
        recommended_films.append({
            'title': film['title'],
            'id': film['id']
        })
    return recommended_films


def get_bulk_recommendations():
    # pylint: disable=no-member
    ids = Film.objects.all().values_list('movie_db_id', flat=True)
    for id in ids:
        recommended = get_recommendations(id)
        film = Film.objects.get(movie_db_id=id)
        recommendation_objects = [Recommendation(movie_db_id=item['id'], title=item['title'],
                                                 film=film) for item in recommended]
        # pylint: disable=no-member
        Recommendation.objects.bulk_create(recommendation_objects)


def store_recommendations(id):
    recommended = get_recommendations(id)
    # pylint: disable=no-member
    film = Film.objects.get(movie_db_id=id)
    recommendation_objects = [Recommendation(movie_db_id=item['id'], title=item['title'],
                                             film=film) for item in recommended]
    # pylint: disable=no-member
    Recommendation.objects.bulk_create(recommendation_objects)


def get_where_to_watch(id):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}/watch/providers', params=payload).json()
    results = {
        'rent': [],
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
        if key == 'rent':
            for option in value:
                results['rent'].append(
                    {option['provider_name']: get_provider_image(option['logo_path'])})
        if key == 'buy':
            for option in value:
                results['buy'].append(
                    {option['provider_name']: get_provider_image(option['logo_path'])})
    return results


def get_film_for_create(id):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}', params=payload).json()
    genres = get_genres_of_film(id)
    keywords = get_keywords(id)
    poster = get_poster(id)
    nb_credits, cast = get_nb_credits(id)
    review = get_review(response.get('title'),
                        response['release_date'].split("-")[0])
    film_object = {
        'title':  response.get('title', None),
        'original_language': response.get('original_language', None),
        'overview': response.get('overview', None),
        'release_date': response.get('release_date', None),
        'popularity': response.get('popularity', None),
        'runtime': response.get('runtime', None),
        'wishlisted': False,
        'budget': response.get('budget', None),
        'revenue': response.get('revenue', None),
        'review_url': review['link']['url'] if review else None,
        'critics_pick': review['critics_pick'] if review else None,
        'review': review['summary_short'] if review else None,
        'vote_average': response.get('vote_average', None),
        'added': True,
        'poster': poster,
        'movie_db_id': response['id'],
    }
    return film_object, genres, keywords, nb_credits, cast


def get_genres_of_film(id):
    payload = {'api_key': movie_api_key}
    details = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}', params=payload)
    genre_results = details.json()['genres']
    return genre_results


def get_genres():
    payload = {'api_key': movie_api_key}
    details = requests.get(
        f'https://api.themoviedb.org/3/genre/movie/list', params=payload)
    genres = details.json()['genres']
    return genres


def get_popular():
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/popular', params=payload).json()['results']
    genres = get_genres()
    for item in response:
        item['genres'] = ", ".join([genre['name']
                                    for genre in genres if genre['id'] in item['genre_ids']])
    return response


def get_top_rated():
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/top_rated', params=payload).json()['results']
    genres = get_genres()
    for item in response:
        item['genres'] = ", ".join([genre['name']
                                    for genre in genres if genre['id'] in item['genre_ids']])
    return response


def get_upcoming_films():
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/upcoming', params=payload).json()['results']
    genres = get_genres()
    for item in response:
        item['genres'] = ", ".join([genre['name']
                                    for genre in genres if genre['id'] in item['genre_ids']])
    return response
