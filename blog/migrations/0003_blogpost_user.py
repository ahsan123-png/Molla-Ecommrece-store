# Generated by Django 4.1.7 on 2024-02-05 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userex_name_userex_useraddress'),
        ('blog', '0002_blogpost_publish_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.userex'),
        ),
    ]
