# Generated by Django 4.0.6 on 2022-08-17 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0006_myuser_is_verify_alter_myuser_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='photo',
            field=models.ImageField(default='users/blank-profile.png', upload_to='users/%Y/%m/%d/'),
        ),
    ]
