# Generated by Django 3.1.3 on 2020-11-06 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0004_auto_20201106_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='date_watched',
            field=models.DateTimeField(null=True, verbose_name='Date Added'),
        ),
    ]
