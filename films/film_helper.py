import requests


def parse_film_search(response):
    films = []
    payload = {'api_key': 'e6b24f5371e6fd462a8a26499fd466b2'}
    # credit = requests.get(
    #     f'https://api.themoviedb.org/3/movie/{response["results"][0]["id"]}/credits', params=payload)
    for item in response['results'][:3]:
        item['genres'] = get_genres(item['id'])
        films.append(item)
    # crew_members = credit.json()['crew']
    # for item in crew_members:
    #     if item['job'] == 'Director':
    #         print(item)
    return films


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
        'title': response['title'],
        'original_language': response['original_language'],
        'overview': response['overview'],
        'release_date': response['release_date'],
        'popularity': response['popularity'],
        'genres': genres,
        'runtime': response['runtime'],
        'budget': response['budget'],
        'revenue': response['revenue'],
        'vote_average': response['vote_average'],
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
