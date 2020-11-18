from django.db import models

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=200)
    known_for = models.CharField(max_length=200, null=True)
    movie_db_id = models.IntegerField(null=True)

    def __str__(self):
        return self.name
