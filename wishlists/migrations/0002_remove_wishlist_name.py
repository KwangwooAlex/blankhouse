# Generated by Django 4.0.10 on 2023-05-19 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlists', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='name',
        ),
    ]
