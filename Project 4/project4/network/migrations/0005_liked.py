# Generated by Django 3.2.9 on 2022-01-23 11:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_alter_following_follower'),
    ]

    operations = [
        migrations.CreateModel(
            name='Liked',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.ManyToManyField(related_name='liked', to='network.Posts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewer', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
