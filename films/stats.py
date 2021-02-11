from .models import Film, Genre, Keyword, CrewCredit, ActingCredit, Recommendation
from .forms import FilmSearchForm, FilmForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg, Max, Q, Count, FloatField
from django.db.models.functions import ExtractYear
from itertools import chain

# thanks to https://gist.github.com/manuganji/6056505


def get_nb_credit_percentages(**filters):
    # pylint: disable=no-member
    film_ids = Film.objects.filter(
        **filters).values_list('id', flat=True)
    # pylint: disable=no-member
    all_jobs = CrewCredit.objects.filter(film__in=film_ids).order_by().values(
        'name', 'job').annotate(avg_rating=Avg('film__vote_average'))

    # x = all_jobs.filter(job='Director').annotate(
    #     Count('job')).order_by('-job__count')
    # print(x)

    num_jobs = all_jobs.count()
    jobs = ['Producer', 'Director', 'Screenplay',
            'Director of Photography', 'Editor', 'Original Music Composer']
    # Make dict of e.g. 'Director : Alfred Hitchcock: 0.2'
    # for j in jobs:
    #     job_percentages = {item['name']: {
    #         'job': j,
    #         'percentage': item['job__count'] * 100/film_ids.count(),
    #         'avg_rating': item['avg_rating']} for item in all_jobs.filter(job=j).annotate(Count('job')).order_by('-job__count')}

    # Remove the leading job title and :
    # and split into individual jobs
    directors = all_jobs.filter(job='Director').annotate(
        Count('job')).order_by('-job__count')

    directors = {item['name']: {
        'job': item['job'],
        'percentage': item['job__count'] * 100 / film_ids.count(),
        'avg_rating': item['avg_rating']} for item in directors
    }

    producers = all_jobs.filter(job='Director').annotate(
        Count('job')).order_by('-job__count')

    producers = {item['name']: {
        'job': item['job'],
        'percentage': item['job__count'] * 100 / film_ids.count(),
        'avg_rating': item['avg_rating']} for item in producers
    }

    screenplays = all_jobs.filter(job='Screenplay').annotate(
        Count('job')).order_by('-job__count')

    screenplays = {item['name']: {
        'job': item['job'],
        'percentage': item['job__count'] * 100 / film_ids.count(),
        'avg_rating': item['avg_rating']} for item in screenplays
    }

    photographers = all_jobs.filter(job='Director of Photography').annotate(
        Count('job')).order_by('-job__count')

    photographers = {item['name']: {
        'job': item['job'],
        'percentage': item['job__count'] * 100 / film_ids.count(),
        'avg_rating': item['avg_rating']} for item in photographers
    }

    editors = all_jobs.filter(job='Editor').annotate(
        Count('job')).order_by('-job__count')

    editors = {item['name']: {
        'job': item['job'],
        'percentage': item['job__count'] * 100 / film_ids.count(),
        'avg_rating': item['avg_rating']} for item in editors
    }

    composers = all_jobs.filter(job='Original Music Composer').annotate(
        Count('job')).order_by('-job__count')

    composers = {item['name']: {
        'job': item['job'],
        'percentage': item['job__count'] * 100 / film_ids.count(),
        'avg_rating': item['avg_rating']} for item in composers
    }

    # Get only first 5
    # thanks to https://stackoverflow.com/questions/7971618/return-first-n-keyvalue-pairs-from-dict
    directors = {A: N for (A, N) in [x for x in directors.items()][:5]}
    screenplays = {A: N for (A, N) in [x for x in screenplays.items()][:5]}
    producers = {A: N for (A, N) in [x for x in producers.items()][:5]}
    photographers = {A: N for (A, N) in [x for x in photographers.items()][:5]}
    editors = {A: N for (A, N) in [x for x in editors.items()][:5]}
    composers = {A: N for (A, N) in [x for x in composers.items()][:5]}

    percentages = {
        'directors': directors,
        'screenwriters': screenplays,
        'photographers': photographers,
        'producers': producers,
        'editors': editors,
        'composers': composers
    }
    return percentages


def get_most_recommended(**filters):
    # pylint: disable=no-member
    user = filters.get('user')
    all_recommendations = Recommendation.objects.filter(
        user=user).values('title', 'movie_db_id')
    print(all_recommendations.count(), 'wooo')
    films = list(Film.objects.filter(
        **filters).values_list('title', flat=True))
    num_recommendations = all_recommendations.count()
    recommendation_percentages = {item['title']: (item['movie_db_id'], item['title__count'] /
                                                  num_recommendations) for item in all_recommendations.annotate(Count('title')).order_by('-title__count') if item['title'] not in films}
    # thanks to https://stackoverflow.com/questions/7971618/return-first-n-keyvalue-pairs-from-dict
    recommendation_percentages = {
        A: N for (A, N) in [x for x in recommendation_percentages.items()][:5]}
    # for key, value in recommendation_percentages.items():
    #     movie_db_ids = list(Genre.objects.filter(name=key).select_related(
    #         'film').values_list('film_id', flat=True))
    #     genre_percentages[key] = (value, Film.objects.filter(
    #         movie_db_id__in=movie_db_ids).aggregate(Avg('vote_average')))
    return recommendation_percentages


def get_genre_percentages(**filters):
    # pylint: disable=no-member
    film_ids = Film.objects.filter(
        **filters).values_list('id', flat=True)
    # pylint: disable=no-member
    all_genres = Genre.objects.filter(film__in=film_ids).values('name')
    num_genres = all_genres.count()
    genre_percentages = {item['name']: item['name__count'] * 100 /
                         film_ids.count() for item in all_genres.annotate(Count('name')).order_by('-name__count')}
    # thanks to https://stackoverflow.com/questions/7971618/return-first-n-keyvalue-pairs-from-dict
    genre_percentages = {
        A: N for (A, N) in [x for x in genre_percentages.items()][:5]}
    for key, value in genre_percentages.items():
        movie_db_ids = list(Genre.objects.filter(name=key).select_related(
            'film').values_list('film_id', flat=True))
        genre_percentages[key] = (value, Film.objects.filter(
            id__in=movie_db_ids, **filters).aggregate(Avg('vote_average')), Film.objects.filter(
            id__in=movie_db_ids, **filters).aggregate(Avg('vote_average')))
    return genre_percentages


def get_film_ratings_by_genre():
    """
        Get the average user score for each genre
    """
    # pylint: disable=no-member
    genres = get_genre_percentages()

    # Film.objects.filter(movie_db_id__in=
    return genres


def get_decade_percentages(**filters):
    # pylint: disable=no-member
    films = Film.objects.filter(**filters).annotate(
        year=ExtractYear('release_date')) if filters else Film.objects.all().annotate(
        year=ExtractYear('release_date'))
    breakdown = {
        '1930s': films.filter(year__gte=1930, year__lte=1939).count() / films.count(),
        '1940s': films.filter(year__gte=1940, year__lte=1949).count() / films.count(),
        '1950s': films.filter(year__gte=1950, year__lte=1959).count() / films.count(),
        '1960s': films.filter(year__gte=1960, year__lte=1969).count() / films.count(),
        '1970s': films.filter(year__gte=1970, year__lte=1979).count() / films.count(),
        '1980s': films.filter(year__gte=1980, year__lte=1989).count() / films.count(),
        '1990s': films.filter(year__gte=1990, year__lte=1999).count() / films.count(),
        '2000s': films.filter(year__gte=2000, year__lte=2009).count() / films.count(),
        '2010s': films.filter(year__gte=2010, year__lte=2019).count() / films.count(),
    }
    return breakdown


def get_headline(**filters):
    genre = list(get_genre_percentages(**filters))[0]
    year = list(get_year_percentages(**filters))[0]
    decade = sorted(get_decade_percentages(
        **filters).values(), reverse=True)[0]
    for key, value in get_decade_percentages(**filters).items():
        if value == decade:
            decade = key
    director = list(get_nb_credit_percentages(
        **filters).get('directors'))[0] if list(get_nb_credit_percentages(
            **filters).get('directors')) else 'N/A'
    actor = list(get_actor_percentages(**filters)
                 )[0] if list(get_actor_percentages(**filters)) else 'N/A'
    return "My most-watched genre is <b>%s</b>. I most often watch <b>%s</b> films, particularly from <b>%s</b>. My most-watched director is <b>%s</b> and my most-watched actor is <b>%s</b>." % (genre, decade, year, director, actor)


def get_year_percentages(**filters):
    # pylint: disable=no-member
    films = Film.objects.filter(
        **filters).annotate(year=ExtractYear('release_date'))
    all_years = films.values('year')
    num_years = all_years.count()
    year_percentages = {item['year']: item['year__count'] /
                        num_years for item in all_years.annotate(Count('year')).order_by('-year__count')}
    # thanks to https://stackoverflow.com/questions/7971618/return-first-n-keyvalue-pairs-from-dict
    year_percentages = {
        A: N for (A, N) in [x for x in year_percentages.items()][:5]}
    return year_percentages


def get_keyword_percentages(**filters):
    # pylint: disable=no-member
    film_ids = Film.objects.filter(
        **filters).values_list('id', flat=True)
    # pylint: disable=no-member
    all_keywords = Keyword.objects.filter(film__in=film_ids).values('name')
    num_keywords = all_keywords.count()
    keyword_percentages = {item['name']: item['name__count'] /
                           num_keywords for item in all_keywords.annotate(Count('name')).order_by('-name__count')}
    # thanks to https://stackoverflow.com/questions/7971618/return-first-n-keyvalue-pairs-from-dict
    keyword_percentages = {
        A: N for (A, N) in [x for x in keyword_percentages.items()][:5]}
    return keyword_percentages


def get_runtime_breakdowns(**filters):
    # pylint: disable=no-member
    films = Film.objects.filter(**filters).values('runtime')
    # pylint: disable=no-member
    breakdown = {
        '60 to 90min': (films.filter(runtime__gte=60, runtime__lte=89).count() / len(films), films.filter(runtime__gte=60, runtime__lte=89).aggregate(Avg('vote_average'))),
        '90 to 120min': (films.filter(runtime__gte=90, runtime__lte=119).count() / len(films), films.filter(runtime__gte=90, runtime__lte=119).aggregate(Avg('vote_average'))),
        '120 to 150min': (films.filter(runtime__gte=120, runtime__lte=149).count() / len(films), films.filter(runtime__gte=120, runtime__lte=149).aggregate(Avg('vote_average'))),
        '150 to 180min': (films.filter(runtime__gte=150, runtime__lte=179).count() / len(films), films.filter(runtime__gte=150, runtime__lte=179).aggregate(Avg('vote_average'))),
        'More than 180min': (films.filter(runtime__gte=180).count() / len(films), films.filter(runtime__gte=180).aggregate(Avg('vote_average'))),
    }
    return breakdown


def get_average_rating(**filters):
    # pylint: disable=no-member
    films = Film.objects.filter(**filters)
    return films.aggregate(Avg('vote_average'))


def get_my_average_score(**filters):
    # pylint: disable=no-member
    films = Film.objects.filter(**filters)
    return films.aggregate(Avg('score'))


def get_actor_percentages(**filters):
    # pylint: disable=no-member
    film_ids = Film.objects.filter(
        **filters).values_list('id', flat=True)
    # pylint: disable=no-member
    all_actors = ActingCredit.objects.filter(film__in=film_ids).order_by().values(
        'movie_db_id', 'name').annotate(avg_rating=Avg('film__vote_average')).annotate(Count('name')).order_by('-name__count')
    num_actors = all_actors.count()
    actor_percentages = {item['name']: {'id': item['movie_db_id'],
                                        'percentage': item['name__count'] * 100 /
                                        film_ids.count(),
                                        'avg_rating': item['avg_rating']} for item in all_actors.annotate(Count('name')).order_by('-name__count')}
    actor_percentages = {
        A: N for (A, N) in [x for x in actor_percentages.items()][:10]}
    return actor_percentages
