# Generated by Django 3.0.7 on 2020-06-25 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0002_remove_reader_mobile'),
    ]

    operations = [
        migrations.CreateModel(
            name='contact_us',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('message', models.TextField(max_length=1000)),
            ],
        ),
    ]