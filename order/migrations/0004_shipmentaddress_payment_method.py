# Generated by Django 4.1.7 on 2024-03-01 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_shipmentaddress_rename_product_order_ordered_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipmentaddress',
            name='payment_method',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]