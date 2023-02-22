# Generated by Django 4.1.6 on 2023-02-22 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='Authors_followers', to='main.author'),
        ),
        migrations.AddField(
            model_name='author',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='Authors_following', to='main.author'),
        ),
        migrations.CreateModel(
            name='FollowRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='main.author')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='main.author')),
            ],
        ),
    ]
