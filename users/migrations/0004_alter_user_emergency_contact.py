# Generated by Django 4.0.10 on 2023-05-23 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_born_year_user_hobby_user_school_user_work'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='emergency_contact',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
