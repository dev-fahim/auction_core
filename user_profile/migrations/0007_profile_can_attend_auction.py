# Generated by Django 4.0.5 on 2022-06-08 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_alter_profile_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='can_attend_auction',
            field=models.BooleanField(default=False),
        ),
    ]
