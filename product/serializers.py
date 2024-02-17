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
            'category',
            'subcategory',
            'productType',
            'productPictures',  # Updated field name
        )
class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductVariant
        fields = (
            'id',
            'product',
            'color',
            'size',
            'stock',
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
class ProductPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductPicture
        fields = ['id', 'picture']