# Generated by Django 3.1.3 on 2020-11-06 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0003_auto_20201106_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='date_watched',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Date Added'),
        ),
        migrations.DeleteModel(
            name='FilmWatched',
        ),
    ]