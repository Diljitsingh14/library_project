# Generated by Django 3.0.1 on 2020-06-13 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0014_auto_20200612_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='reading_record',
            name='total_page',
            field=models.IntegerField(default=0),
        ),
    ]