# Generated by Django 4.0.10 on 2023-05-19 20:27

from django.db import migrations, models
import photos.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('picture', models.FileField(upload_to='media/', validators=[photos.validators.validate_file_size])),
                ('description', models.CharField(blank=True, max_length=140, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
