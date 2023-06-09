# Generated by Django 4.1 on 2023-02-06 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_wishlist_listing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.BooleanField()),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statut', related_query_name='statut', to='auctions.listing', unique=True)),
            ],
        ),
    ]
