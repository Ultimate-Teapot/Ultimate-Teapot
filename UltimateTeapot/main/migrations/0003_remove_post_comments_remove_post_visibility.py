# Generated by Django 4.1.7 on 2023-03-27 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_post_markdown_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='post',
            name='visibility',
        ),
    ]
