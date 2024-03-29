# Generated by Django 4.1.7 on 2024-01-06 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('order', '0002_initial'),
        ('payment', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasehistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userex'),
        ),
        migrations.AddField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order'),
        ),
    ]
