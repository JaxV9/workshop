# Generated by Django 4.1 on 2023-05-31 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_watchlist_gift_exchange'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange',
            name='delete',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
