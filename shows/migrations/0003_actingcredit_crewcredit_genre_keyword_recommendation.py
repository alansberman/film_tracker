# Generated by Django 3.1.3 on 2020-12-04 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0002_show_date_watched'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('movie_db_id', models.IntegerField()),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shows.show')),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('movie_db_id', models.IntegerField()),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shows.show')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('movie_db_id', models.IntegerField()),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shows.show')),
            ],
        ),
        migrations.CreateModel(
            name='CrewCredit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('job', models.CharField(max_length=200)),
                ('movie_db_id', models.IntegerField()),
                ('credit_id', models.CharField(max_length=200, null=True)),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shows.show')),
            ],
        ),
        migrations.CreateModel(
            name='ActingCredit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('role', models.CharField(max_length=200)),
                ('movie_db_id', models.IntegerField()),
                ('credit_id', models.CharField(max_length=200, null=True)),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shows.show')),
            ],
        ),
    ]