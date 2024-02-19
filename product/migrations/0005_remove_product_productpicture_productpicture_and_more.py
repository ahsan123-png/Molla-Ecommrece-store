# Generated by Django 4.1.7 on 2024-02-16 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_productpicture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='productPicture',
        ),
        migrations.CreateModel(
            name='ProductPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='product_images/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='product.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='productPictures',
            field=models.ManyToManyField(related_name='products', to='product.productpicture'),
        ),
    ]
