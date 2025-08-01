from django import forms
from .models import Product, ProductPicture, ProductVariant

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name', 'description', 'brand', 'price',
            'category', 'subcategory', 'productType', 'productPictures'
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full'}),
            'brand': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'price': forms.NumberInput(attrs={'class': 'input input-bordered w-full'}),
            'category': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'subcategory': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'productType': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'productPictures': forms.SelectMultiple(attrs={'class': 'select select-bordered w-full'}),
        }
