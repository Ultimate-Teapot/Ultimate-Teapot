# Generated by Django 4.1.7 on 2023-03-19 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_post_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_id',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
        ),
    ]
