# Generated by Django 4.1.5 on 2023-02-24 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_bid_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='current_bid',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True),
        ),
    ]