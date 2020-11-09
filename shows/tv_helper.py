import requests


def parse_search(response, query):
    shows = []
    people = []
    # credit = requests.get(
    #     f'https://api.themoviedb.org/3/movie/{response["results"][0]["id"]}/credits', params=payload)
    for item in response['results'][:10]:
        if item['media_type'] == 'tv':
            shows.append(parse_search_item(item, query))
        elif item['media_type'] == 'person':
            people.append(parse_search_item(item, query))
    # crew_members = credit.json()['crew']
    # for item in crew_members:
    #     if item['job'] == 'Director':
    #         print(item)
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
    payload = {'api_key': 'e6b24f5371e6fd462a8a26499fd466b2'}
    details = requests.get(
        f'https://api.themoviedb.org/3/genre/tv/list', params=payload)
    genres = details.json()['genres']
    return genres


def get_cast(id):
    payload = {'api_key': 'e6b24f5371e6fd462a8a26499fd466b2'}
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
    payload = {'api_key': 'e6b24f5371e6fd462a8a26499fd466b2'}
    response = requests.get(
        f'https://api.themoviedb.org/3/tv/{show_id}/season/{season_number}', params=payload).json()
    return response


def get_episode(show_id, season_number, episode_number):
    payload = {'api_key': 'e6b24f5371e6fd462a8a26499fd466b2'}
    response = requests.get(
        f'https://api.themoviedb.org/3/tv/{show_id}/season/{season_number}/episode/{episode_number}', params=payload).json()
    return response


def get_show_details(id):
    payload = {'api_key': 'e6b24f5371e6fd462a8a26499fd466b2'}
    response = requests.get(
        f'https://api.themoviedb.org/3/tv/{id}', params=payload).json()
    response['genres'] = ", ".join([genre['name']
                                    for genre in response['genres']])
    return response


def get_recommendations(id):
    payload = {'api_key': 'e6b24f5371e6fd462a8a26499fd466b2'}
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
    return 'https://image.tmdb.org/t/p/original'+show['backdrop_path']
