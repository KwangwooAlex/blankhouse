# Generated by Django 4.0.10 on 2023-09-22 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='details',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='details',
            field=models.TextField(),
        ),
    ]
