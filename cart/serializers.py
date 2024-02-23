from rest_framework import serializers
from .models import Cart, Wishlist
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id',
                'user',
                'product',
                'quantity', 
                'date_added',
                'subtotal']

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id',
                'user',
                'product', 
                'date_added',
                'color',
                'size', 
                'quantity']
