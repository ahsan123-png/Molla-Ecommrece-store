from rest_framework import serializers
from . import models

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = (
            'id',
            'product_name',
            'description',
            'brand',
            'price',
            'color',
            'size',
            'stock',
            'category',
            'subcategory',
            'productType',
            'productPicture',
        )

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductReview
        fields = (
            'id',
            'product',
            'user',
            'title',
            'content',
            'rating',
            'created_at',
        )

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = (
            'id',
            'product',
            'stock_quantity',
        )
