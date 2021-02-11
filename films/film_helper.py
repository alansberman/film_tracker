import csv
from .models import Film, Recommendation, ActingCredit, CrewCredit, Genre, Keyword
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from datetime import date
import os
import urllib


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
    if 'results' in response and response['num_results'] > 0:
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


def save_film(film, genres, keywords, nb_credits, cast, wishlisted=False, date_watched=date.today(), score=None, added=False, comments=None, liked=None, user=1):
    film_to_save = Film(title=film['title'],
                        original_language=film['original_language'],
                        overview=film['overview'],
                        popularity=film['popularity'],
                        runtime=film['runtime'],
                        budget=film['budget'],
                        revenue=film['revenue'],
                        vote_average=film['vote_average'],
                        added=added,
                        score=score,
                        user=user,
                        comments=comments,
                        date_watched=date_watched,
                        release_date=film['release_date'],
                        movie_db_id=film['movie_db_id'],
                        poster=film['poster'],
                        wishlisted=wishlisted,
                        liked=liked,
                        review=film['review'],
                        review_url=film['review_url'],
                        critics_pick=film['critics_pick'],
                        )
    film_to_save.save()

    store_recommendations(film['movie_db_id'], user)

    genre_objects = [Genre(movie_db_id=item['id'], name=item['name'],
                           film=film_to_save, user=user) for item in genres]
    # pylint: disable=no-member
    Genre.objects.bulk_create(genre_objects)
    keyword_objects = [Keyword(
        movie_db_id=item['id'], name=item['name'], film=film_to_save, user=user) for item in keywords]
    # pylint: disable=no-member
    Keyword.objects.bulk_create(keyword_objects)
    credit_objects = [CrewCredit(movie_db_id=item['id'], name=item['name'], film=film_to_save,
                                 job=item['job'], credit_id=item['credit_id'], user=user) for item in nb_credits]
    # pylint: disable=no-member
    CrewCredit.objects.bulk_create(credit_objects)
    acting_objects = [ActingCredit(movie_db_id=item['id'], name=item['name'], film=film_to_save,
                                   role=item['role'], credit_id=item['credit_id'], user=user) for item in cast]
    # pylint: disable=no-member
    ActingCredit.objects.bulk_create(acting_objects)


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


def store_recommendations(id, user=None):
    recommended = get_recommendations(id)
    # pylint: disable=no-member
    film = Film.objects.filter(movie_db_id=id).first()
    recommendation_objects = [Recommendation(movie_db_id=item['id'], title=item['title'],
                                             film=film, user=user) for item in recommended]
    # pylint: disable=no-member
    Recommendation.objects.bulk_create(recommendation_objects)


def get_where_to_watch(id):
    payload = {'api_key': movie_api_key}
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}/watch/providers', params=payload).json()
    results = {}
    for key, value in response['results'].items():
        results[key] = {
            'rent': [],
            'buy': [],
            'watch': []
        }
        for k, v in value.items():
            if k == 'flatrate':
                for option in v:
                    results[key]['watch'].append(
                        {option['provider_name']: get_provider_image(option['logo_path'])})
            if k == 'rent':
                for option in v:
                    results[key]['rent'].append(
                        {option['provider_name']: get_provider_image(option['logo_path'])})
            if k == 'buy':
                for option in v:
                    results[key]['buy'].append(
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


def bulk_create_films(request):
    films = []
    user = request.user if request.user else 1
    with open('contemporary.csv', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                if row[0] == '' or 'NOTE: ' in row[0]:
                    continue
                name = row[0]
                liked = '*' in row[0]
                name = name.replace("(S)", "")
                year = row[1]
                name = name.replace("*", "")
                films.append({
                    'title': name,
                    'liked': liked,
                    'year': year
                })
                line_count += 1
        for film in films:
            payload = {
                'api_key': movie_api_key, 'query': film['title']}
            response = requests.get(
                'https://api.themoviedb.org/3/search/movie', params=payload).json()
            if 'results' in response and len(response['results']) >= 1:
                for item in response['results']:
                    if 'release_date' in item:
                        if len(item['release_date']) >= 4:
                            if abs(eval(item['release_date'].split('-')[0]) - eval(film['year'])) <= 1:
                                film_object, genres, keywords, nb_credits, cast = get_film_for_create(
                                    item['id'])
                                save_film(film_object, genres, keywords, nb_credits, cast, wishlisted=False, date_watched=date.today(
                                ), score=None, added=True, comments=None, liked=film['liked'], user=user)
                                break


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


def discover(**filters):
    payload = {'api_key': movie_api_key}
    payload = {**payload, **filters}
    response = requests.get(
        f'https://api.themoviedb.org/3/discover/movie', params=payload)
    return response.json()['results']
