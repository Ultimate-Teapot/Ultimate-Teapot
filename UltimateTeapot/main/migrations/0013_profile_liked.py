# Generated by Django 4.1.7 on 2023-03-31 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_like_author_remove_like_post_comment_post_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='liked',
            field=models.ManyToManyField(to='main.like'),
        ),
    ]
