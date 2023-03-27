# Generated by Django 4.1.7 on 2023-03-27 08:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField()),
                ('object_id', models.CharField(max_length=255)),
                ('actor', models.CharField(max_length=255)),
                ('object', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('type', models.CharField(default='Author', editable=False, max_length=100)),
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('url', models.URLField()),
                ('host', models.URLField()),
                ('displayName', models.CharField(max_length=100)),
                ('github', models.URLField()),
                ('profileImage', models.URLField()),
                ('last_date', models.DateField(default=datetime.datetime.now)),
                ('followers', models.ManyToManyField(blank=True, related_name='users_following', to='main.profile')),
                ('friends', models.ManyToManyField(blank=True, related_name='friends_with', to='main.profile')),
                ('inbox', models.ManyToManyField(to='main.object')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('type', models.CharField(default='post', editable=False, max_length=100)),
                ('title', models.TextField()),
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('source', models.URLField()),
                ('origin', models.URLField()),
                ('description', models.TextField(blank=True)),
                ('contentType', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('markdown_content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('categories', models.CharField(default=['web', 'tutorial'], max_length=200)),
                ('count', models.IntegerField(default=0)),
                ('comments', models.CharField(max_length=255)),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now)),
                ('visibility', models.CharField(default='PUBLIC', max_length=10)),
                ('unlisted', models.BooleanField(default=False)),
                ('likes', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.CharField(max_length=255)),
                ('author_id', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('like_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_post_like', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to='main.post')),
            ],
        ),
        migrations.CreateModel(
            name='FollowRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor', models.CharField(max_length=255)),
                ('object', models.CharField(max_length=255)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('content', models.TextField()),
                ('contentType', models.TextField(default='text/markdown', max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('comment_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_post_comment', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='main.post')),
            ],
        ),
    ]
