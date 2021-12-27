# Generated by Django 3.2.9 on 2021-12-22 08:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.CharField(editable=False, max_length=500),
        ),
        migrations.AlterField(
            model_name='comment',
            name='subject',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='writer', to='auctions.listings'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='writer',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='writer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lists', models.ManyToManyField(to='auctions.Listings')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watcher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]