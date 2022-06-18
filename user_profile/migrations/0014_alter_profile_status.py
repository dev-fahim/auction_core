# Generated by Django 4.0.5 on 2022-06-17 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0013_profile_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(choices=[('NOT_SUBMITTED', 'Not Submitted'), ('IN_PROGRESS', 'In Progress'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='NOT_SUBMITTED', max_length=50),
        ),
    ]
