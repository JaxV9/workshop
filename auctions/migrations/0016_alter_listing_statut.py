# Generated by Django 4.1 on 2023-02-06 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_listing_statut_delete_statut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='statut',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
