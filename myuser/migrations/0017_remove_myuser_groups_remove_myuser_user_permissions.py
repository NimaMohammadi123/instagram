# Generated by Django 4.0.6 on 2022-09-29 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0016_alter_myuser_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='user_permissions',
        ),
    ]