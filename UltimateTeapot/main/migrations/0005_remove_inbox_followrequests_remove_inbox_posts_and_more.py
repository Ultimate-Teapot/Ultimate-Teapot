# Generated by Django 4.1.7 on 2023-03-22 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_followrequest_inbox_followrequests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inbox',
            name='followRequests',
        ),
        migrations.RemoveField(
            model_name='inbox',
            name='posts',
        ),
        migrations.AddField(
            model_name='inbox',
            name='data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
