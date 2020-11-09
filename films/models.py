from django.db import models

# Create your models here.


class Film(models.Model):
    title = models.CharField(max_length=200)
    original_language = models.CharField(max_length=200)
    overview = models.TextField(null=True)
    movie_db_id = models.IntegerField(null=True)
    release_date = models.CharField(max_length=200)
    comments = models.CharField(max_length=200, null=True)
    popularity = models.TextField(null=True)
    genres = models.CharField(max_length=200, null=True)
    runtime = models.IntegerField(null=True)
    budget = models.IntegerField(null=True)
    revenue = models.IntegerField(null=True)
    vote_average = models.FloatField(null=True)
    added = models.BooleanField(null=True)
    wishlisted = models.BooleanField(null=True)
    score = models.FloatField(null=True)
    date_watched = models.DateTimeField('Date Added', null=True)

    def __str__(self):
        return self.title


# class FilmWatched(models.Model):
#     film = models.ForeignKey(Film, on_delete=models.CASCADE)
#     date_watched = models.DateTimeField('Date Added', auto_now=True, null=True)

#     def __str__(self):
#         return "Watched %s on %s" % (self.film, self.date_watched)
