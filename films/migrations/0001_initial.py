# Generated by Django 3.1.3 on 2020-11-05 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('original_language', models.CharField(max_length=200)),
                ('overview', models.TextField(null=True)),
                ('release_date', models.CharField(max_length=200)),
                ('popularity', models.IntegerField(null=True)),
                ('genres', models.JSONField()),
                ('runtime', models.IntegerField(null=True)),
                ('budget', models.IntegerField(null=True)),
                ('revenue', models.IntegerField(null=True)),
                ('date_watched', models.CharField(max_length=200)),
                ('vote_average', models.FloatField(null=True)),
                ('vote_count', models.IntegerField(null=True)),
                ('score', models.FloatField()),
            ],
        ),
    ]
