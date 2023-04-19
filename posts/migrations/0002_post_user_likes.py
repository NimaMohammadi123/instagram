# Generated by Django 4.0.6 on 2022-08-21 19:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user_likes',
            field=models.ManyToManyField(blank=True, related_name='posts_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
