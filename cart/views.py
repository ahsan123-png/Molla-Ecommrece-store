from django.shortcuts import render
# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from users.models import UserEx
from .models import Wishlist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
@csrf_exempt
def addToWishlist(request):
    if request.method == 'POST':
        user = request.user
        if isinstance(user, UserEx):  # Check if the user is an instance of UserEx
            user_ex = user
        else:
            # If the user is not an instance of UserEx, try to retrieve the UserEx instance
            user_ex =UserEx.objects.get(id=user.id)
        product_id = request.POST.get('product_id')
        color = request.POST.get('color_select')
        size = request.POST.get('size')
        quantity = request.POST.get('quantity', 1)
        if Wishlist.objects.filter(user=user, product_id=product_id, color=color, size=size).exists():
            return JsonResponse({'error': 'Product already exists in wishlist'}, status=400)
        wishlist_item = Wishlist.objects.create(
            user=user_ex,
            product_id=product_id,
            color=color,
            size=size,
            quantity=quantity
        )
        wishlist_item.save()
        return JsonResponse({'message': 'Product added to wishlist successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def cart(request):
    return render(request,"cart.html")


def wishlist(request):
    # Get the user's wishlist items
    wishlist_items = Wishlist.objects.filter(user=request.user)
    products_info = []
    for item in wishlist_items:
        product = item.product
        product_info = {
            'name': product.product_name,
            'price': product.price,
            'availability': 'In stock' if product.inventory.stock_quantity > 0 else 'Out of stock',
            'image': None 
        }
        if product.pictures.exists():
            product_info['image'] = product.pictures.first().picture.url
        products_info.append(product_info)
    return render(request, 'wishlist.html', {'products_info': products_info})


