# Generated by Django 3.0 on 2020-05-10 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_auto_20200510_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='thumbnail',
        ),
    ]