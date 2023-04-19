# Generated by Django 4.0.6 on 2022-09-23 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_postcomment'),
        ('myuser', '0008_contact_myuser_following_contact_user_from_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='save_post',
            field=models.ManyToManyField(related_name='save_post', to='posts.post'),
        ),
    ]