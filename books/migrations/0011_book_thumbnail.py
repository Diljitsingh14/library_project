# Generated by Django 3.0 on 2020-05-20 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_remove_book_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='thumbnail',
            field=models.CharField(default='', max_length=200, unique=True),
        ),
    ]