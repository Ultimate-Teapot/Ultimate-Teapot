# Generated by Django 4.1.7 on 2023-04-01 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_comment_author_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment_author',
        ),
    ]