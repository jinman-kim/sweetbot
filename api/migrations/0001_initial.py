# Generated by Django 3.0.5 on 2023-05-17 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('image', models.TextField()),
                ('profile_image', models.TextField()),
                ('user_id', models.TextField()),
                ('like_count', models.TextField()),
            ],
        ),
    ]
