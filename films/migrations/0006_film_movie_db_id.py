# Generated by Django 3.1.3 on 2020-11-06 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0005_auto_20201106_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='movie_db_id',
            field=models.IntegerField(null=True),
        ),
    ]
