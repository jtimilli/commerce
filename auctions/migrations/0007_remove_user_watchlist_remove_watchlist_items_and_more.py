# Generated by Django 4.1.5 on 2023-02-22 20:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_rename_watchlist_watchlist_items_user_watchlist_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='watchlist',
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='items',
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='WatchlistItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.auctionlisting')),
                ('watchlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.watchlist')),
            ],
            options={
                'unique_together': {('listing', 'watchlist')},
            },
        ),
        migrations.AddField(
            model_name='watchlist',
            name='listings',
            field=models.ManyToManyField(through='auctions.WatchlistItem', to='auctions.auctionlisting'),
        ),
    ]
