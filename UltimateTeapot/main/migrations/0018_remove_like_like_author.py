# Generated by Django 4.1.7 on 2023-04-01 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_remove_comment_comment_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='like_author',
        ),
    ]
