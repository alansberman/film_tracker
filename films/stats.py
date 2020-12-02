from .models import Film, Genre, Keyword, CrewCredit, ActingCredit, Recommendation
from .forms import FilmSearchForm, FilmForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg, Max, Q, Count, FloatField
from django.db.models.functions import ExtractYear


# thanks to https://gist.github.com/manuganji/6056505
def get_nb_credit_percentages():
    # pylint: disable=no-member
    all_jobs = CrewCredit.objects.all().values('job', 'name', 'movie_db_id')
    num_jobs = all_jobs.count()
    jobs = ['Producer', 'Director', 'Screenplay',
            'Director of Photography', 'Editor', 'Original Music Composer']
    # Make dict of e.g. 'Director : Alfred Hitchcock: 0.2'
    job_percentages = {item['job']+' : '+item['name']: {item['movie_db_id']: item['job__count'] * 100/num_jobs}
                       for item in all_jobs.annotate(Count('job')).order_by('-job__count') if item['job'] in jobs}
    # Remove the leading job title and :
    # and split into individual jobs
    directors = {k[k.index(':')+2:]: v for k, v in job_percentages.items(
    ) if 'Director' in k and 'Photography' not in k}
    producers = {k[k.index(':')+2:]: v for k,
                 v in job_percentages.items() if 'Producer' in k}
    screenplays = {k[k.index(':')+2:]: v for k, v in job_percentages.items()
                   if 'Screenplay' in k}
    photographers = {k[k.index(':')+2:]: v for k, v in job_percentages.items()
                     if 'Photography' in k}
    editors = {k[k.index(':')+2:]: v for k, v in job_percentages.items()
               if 'Editor' in k}
    composers = {k[k.index(':')+2:]: v for k, v in job_percentages.items()
                 if 'Original Music Composer' in k}
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


def get_most_recommended():
    # pylint: disable=no-member
    all_recommendations = Recommendation.objects.all().values('title', 'movie_db_id')
    films = list(Film.objects.all().values_list('title', flat=True))
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


def get_genre_percentages():
    # pylint: disable=no-member
    all_genres = Genre.objects.all().values('name')
    num_genres = all_genres.count()
    genre_percentages = {item['name']: item['name__count'] /
                         num_genres for item in all_genres.annotate(Count('name')).order_by('-name__count')}
    # thanks to https://stackoverflow.com/questions/7971618/return-first-n-keyvalue-pairs-from-dict
    genre_percentages = {
        A: N for (A, N) in [x for x in genre_percentages.items()][:5]}
    for key, value in genre_percentages.items():
        movie_db_ids = list(Genre.objects.filter(name=key).select_related(
            'film').values_list('film_id', flat=True))
        genre_percentages[key] = (value, Film.objects.filter(
            movie_db_id__in=movie_db_ids).aggregate(Avg('vote_average')))
    return genre_percentages


def get_film_ratings_by_genre():
    """
        Get the average user score for each genre
    """
    # pylint: disable=no-member
    genres = get_genre_percentages()

    # Film.objects.filter(movie_db_id__in=
    return genres


def get_decade_percentages():
    # pylint: disable=no-member
    films = Film.objects.annotate(year=ExtractYear('release_date'))
    breakdown = {
        '1930s': films.filter(year__gte=1930, year__lte=1939).count() / len(films),
        '1940s': films.filter(year__gte=1940, year__lte=1949).count() / len(films),
        '1950s': films.filter(year__gte=1950, year__lte=1959).count() / len(films),
        '1960s': films.filter(year__gte=1960, year__lte=1969).count() / len(films),
        '1970s': films.filter(year__gte=1970, year__lte=1979).count() / len(films),
        '1980s': films.filter(year__gte=1980, year__lte=1989).count() / len(films),
        '1990s': films.filter(year__gte=1990, year__lte=1999).count() / len(films),
        '2000s': films.filter(year__gte=2000, year__lte=2009).count() / len(films),
        '2010s': films.filter(year__gte=2010, year__lte=2019).count() / len(films),
    }
    return breakdown


def get_headline():
    genre = list(get_genre_percentages())[0]
    year = list(get_year_percentages())[0]
    decade = sorted(get_decade_percentages().values(), reverse=True)[0]
    for key, value in get_decade_percentages().items():
        if value == decade:
            decade = key
    director = list(get_nb_credit_percentages().get('directors'))[0]
    actor = list(get_actor_percentages())[0]
    return "My most-watched genre is <b>%s</b>. I most often watch <b>%s</b> films, particularly from <b>%s</b>. My most-watched director is <b>%s</b> and my most-watched actor is <b>%s</b>." % (genre, decade, year, director, actor)


def get_year_percentages():
    # pylint: disable=no-member
    films = Film.objects.annotate(year=ExtractYear('release_date'))
    all_years = films.values('year')
    num_years = all_years.count()
    year_percentages = {item['year']: item['year__count'] /
                        num_years for item in all_years.annotate(Count('year')).order_by('-year__count')}
    # thanks to https://stackoverflow.com/questions/7971618/return-first-n-keyvalue-pairs-from-dict
    year_percentages = {
        A: N for (A, N) in [x for x in year_percentages.items()][:5]}
    return year_percentages


def get_keyword_percentages():
    # pylint: disable=no-member
    all_keywords = Keyword.objects.all().values('name')
    num_keywords = all_keywords.count()
    keyword_percentages = {item['name']: item['name__count'] /
                           num_keywords for item in all_keywords.annotate(Count('name')).order_by('-name__count')}
    # thanks to https://stackoverflow.com/questions/7971618/return-first-n-keyvalue-pairs-from-dict
    keyword_percentages = {
        A: N for (A, N) in [x for x in keyword_percentages.items()][:5]}
    return keyword_percentages


def get_runtime_breakdowns():
    # pylint: disable=no-member
    films = Film.objects.all().values('runtime')
    # pylint: disable=no-member
    breakdown = {
        '60 to 90min': (Film.objects.filter(runtime__gte=60, runtime__lte=89).count() / len(films), Film.objects.filter(runtime__gte=60, runtime__lte=89).aggregate(Avg('vote_average'))),
        '90 to 120min': (Film.objects.filter(runtime__gte=90, runtime__lte=119).count() / len(films), Film.objects.filter(runtime__gte=90, runtime__lte=119).aggregate(Avg('vote_average'))),
        '120 to 150min': (Film.objects.filter(runtime__gte=120, runtime__lte=149).count() / len(films), Film.objects.filter(runtime__gte=120, runtime__lte=149).aggregate(Avg('vote_average'))),
        '150 to 180min': (Film.objects.filter(runtime__gte=150, runtime__lte=179).count() / len(films), Film.objects.filter(runtime__gte=150, runtime__lte=179).aggregate(Avg('vote_average'))),
        'More than 180min': (Film.objects.filter(runtime__gte=180).count() / len(films), Film.objects.filter(runtime__gte=180).aggregate(Avg('vote_average'))),
    }
    return breakdown


def get_average_rating():
    # pylint: disable=no-member
    films = Film.objects.all()
    return films.aggregate(Avg('vote_average'))


def get_actor_percentages():
    # pylint: disable=no-member
    all_actors = ActingCredit.objects.all().values('name', 'movie_db_id')
    num_actors = len(all_actors)
    actor_percentages = {item['name']: {item['movie_db_id']: item['name__count'] * 100 /
                                        num_actors} for item in all_actors.annotate(Count('name')).order_by('-name__count')}
    actor_percentages = {
        A: N for (A, N) in [x for x in actor_percentages.items()][:10]}
    return actor_percentages
