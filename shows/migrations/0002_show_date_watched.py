# Generated by Django 3.1.3 on 2020-11-10 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='date_watched',
            field=models.DateField(null=True),
        ),
    ]
