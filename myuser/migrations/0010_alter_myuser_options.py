# Generated by Django 4.0.6 on 2022-09-29 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0009_myuser_save_post'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'default_permissions': (), 'permissions': (('add_MyUser', 'Can add foo'), ('change_MyUser', 'Can change foo'), ('delete_MyUser', 'Can delete foo'), ('view_MyUser', 'Can view foo'), ('list_MyUser', 'Can list all foo'))},
        ),
    ]