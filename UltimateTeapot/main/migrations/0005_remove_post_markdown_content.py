# Generated by Django 4.1.7 on 2023-03-27 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_post_comments_post_markdown_content_post_visibility'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='markdown_content',
        ),
    ]