# Generated by Django 4.1.6 on 2023-02-22 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_author_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='followers',
            field=models.ManyToManyField(blank=True, to='main.author'),
        ),
    ]
