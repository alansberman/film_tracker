from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.


class Film(models.Model):
    user = models.ForeignKey(User, verbose_name='User',
                             related_name='films', on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    original_language = models.CharField(max_length=200)
    overview = models.TextField(null=True)
    movie_db_id = models.IntegerField(null=True)
    release_date = models.DateField(null=True)
    comments = models.CharField(max_length=200, null=True)
    popularity = models.TextField(null=True)
    runtime = models.IntegerField(null=True)
    budget = models.IntegerField(null=True)
    revenue = models.IntegerField(null=True)
    vote_average = models.FloatField(null=True)
    liked = models.BooleanField(null=True)
    added = models.BooleanField(null=True)
    wishlisted = models.BooleanField(null=True)
    score = models.FloatField(null=True)
    review = models.TextField(null=True)
    review_url = models.CharField(max_length=300, null=True)
    critics_pick = models.BooleanField(null=True)
    poster = models.CharField(max_length=200, null=True)
    date_watched = models.DateTimeField('Date Added', null=True)

    def __str__(self):
        return self.title


class ActingCredit(models.Model):
    user = models.ForeignKey(User, verbose_name='User',
                             related_name='actors', on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, null=True)
    movie_db_id = models.IntegerField()
    credit_id = models.CharField(max_length=200, null=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    def __str__(self):
        return '%s as %s in %s' % (self.name, self.role, self.film)


class Genre(models.Model):
    user = models.ForeignKey(User, verbose_name='User',
                             related_name='genres', on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200)
    movie_db_id = models.IntegerField()
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Recommendation(models.Model):
    user = models.ForeignKey(User, verbose_name='User',
                             related_name='recommendations', on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    movie_db_id = models.IntegerField()
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Keyword(models.Model):
    user = models.ForeignKey(User, verbose_name='User',
                             related_name='keywords', on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200)
    movie_db_id = models.IntegerField()
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CrewCredit(models.Model):
    user = models.ForeignKey(User, verbose_name='User',
                             related_name='credits', on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200)
    job = models.CharField(max_length=200)
    movie_db_id = models.IntegerField()
    credit_id = models.CharField(max_length=200, null=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    def __str__(self):
        return '%s as %s in %s' % (self.name, self.job, self.film)


class Token(models.Model):
    user = models.ForeignKey(User, verbose_name='User',
                             related_name='token', on_delete=models.CASCADE, default=1)
    value = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    expiry = models.DateTimeField()
    valid = models.BooleanField(default=True)

    def __str__(self):
        return str(self.value)
