# Generated by Django 4.1.7 on 2024-02-27 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_alter_wishlist_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='color',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='cart',
            name='size',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
