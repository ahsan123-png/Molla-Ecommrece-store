from django.contrib import admin
from .models import Product, ProductVariant, ProductPicture, ProductReview, Inventory

class ProductPictureInline(admin.TabularInline):
    model = ProductPicture
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'brand', 'category', 'price', 'productType']
    search_fields = ['product_name', 'brand', 'category']
    list_filter = ['category', 'brand', 'productType']
    inlines = [ProductPictureInline, ProductVariantInline]
    fieldsets = (
        ("Basic Info", {
            'fields': ('product_name', 'description', 'brand', 'price')
        }),
        ("Classification", {
            'fields': ('category', 'subcategory', 'productType')
        }),
    )

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['title', 'content']

class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'stock_quantity']
    search_fields = ['product__product_name']

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Inventory, InventoryAdmin)
