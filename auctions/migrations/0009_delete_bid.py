# Generated by Django 4.1.5 on 2023-02-24 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_bid_unique_together'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bid',
        ),
    ]
