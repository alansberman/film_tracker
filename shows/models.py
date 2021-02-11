from django.db import models

# Create your models here.


class Show(models.Model):
    name = models.CharField(max_length=200)
    original_language = models.CharField(max_length=200)
    original_name = models.CharField(max_length=200)
    type_of_show = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    overview = models.TextField(null=True)
    movie_db_id = models.IntegerField(null=True)
    comments = models.CharField(max_length=200, null=True)
    popularity = models.FloatField(null=True)
    number_of_seasons = models.IntegerField(null=True)
    number_of_episodes = models.IntegerField(null=True)
    runtime = models.IntegerField(null=True)
    first_air_date = models.DateField(null=True)
    vote_average = models.FloatField(null=True)
    date_watched = models.DateField(null=True)
    added = models.BooleanField(null=True)
    wishlisted = models.BooleanField(null=True)
    score = models.FloatField(null=True)

    def __str__(self):
        return self.name


class Season(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    season_number = models.IntegerField()
    overview = models.CharField(max_length=200, null=True)
    movie_db_id = models.IntegerField()
    number_of_episodes = models.IntegerField()

    def __str__(self):
        return '%s season %s' % (self.show.name, self.season_number)


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    season_number = models.IntegerField()
    overview = models.CharField(max_length=200, null=True)
    movie_db_id = models.IntegerField()
    episode_number = models.IntegerField()

    def __str__(self):
        return '%s episode %s' % (self.season.name, self.episode_number)


class Genre(models.Model):
    name = models.CharField(max_length=200)
    movie_db_id = models.IntegerField()
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Recommendation(models.Model):
    name = models.CharField(max_length=200)
    movie_db_id = models.IntegerField()
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CrewCredit(models.Model):
    name = models.CharField(max_length=200)
    known_for = models.CharField(
        max_length=200, null=True, default='Production')
    job = models.CharField(max_length=200)
    movie_db_id = models.IntegerField()
    credit_id = models.CharField(max_length=200, null=True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    def __str__(self):
        return '%s as %s in %s' % (self.name, self.job, self.show)


class ActingCredit(models.Model):
    name = models.CharField(max_length=200)
    character = models.CharField(max_length=200)
    movie_db_id = models.IntegerField()
    credit_id = models.CharField(max_length=200, null=True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    def __str__(self):
        return '%s as %s in %s' % (self.name, self.character, self.show)
