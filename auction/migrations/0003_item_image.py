# Generated by Django 5.1.6 on 2025-02-25 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0002_item_bid_count_item_likes_count_item_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='items/'),
        ),
    ]
