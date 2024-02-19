from django.shortcuts import redirect, render
# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from product.models import Product
from users.models import UserEx
from .models import Cart, Wishlist
from django.views.decorators.csrf import csrf_exempt
# ==========================================
def cart(request):
    return render(request,"cart.html")
# ==== add items to wishlist page =====
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
# ===== Get data from wishlist ======
def wishlist(request):
    # Get the user's wishlist items
    wishlist_items = Wishlist.objects.filter(user=request.user)
    products_info = []
    for item in wishlist_items:
        product = item.product
        product_info = {
            'wishlist_id': item.id,
            'name': product.product_name,
            'price': product.price,
            'availability': 'In stock' if product.inventory.stock_quantity > 0 else 'Out of stock',
            'image': None 
        }
        if product.pictures.exists():
            product_info['image'] = product.pictures.first().picture.url
        products_info.append(product_info)
    return render(request, 'wishlist.html', {'products_info': products_info})
#==== add wishlist item to cart ======
@csrf_exempt
def addCart(request, id):
    if request.method == "POST":
        wishlist_item = Wishlist.objects.get(id=id)
        cart_item, created = Cart.objects.get_or_create(
            user=wishlist_item.user,
            product=wishlist_item.product,
            defaults={
                'quantity': wishlist_item.quantity,
                'subtotal': wishlist_item.quantity * wishlist_item.product.price
            }
        )
        if not created:
            cart_item.quantity += wishlist_item.quantity
            cart_item.subtotal += wishlist_item.quantity * wishlist_item.product.price
            cart_item.save()
        wishlist_item.delete()
        return redirect('cart')
# == add a product into cart ===
@csrf_exempt
def addProductToCart(request, id):
    if request.method == "GET":
        try:
            product_item = Product.objects.get(id=id)
            user = request.user
            if isinstance(user, UserEx):
                user_ex = user
            else:
                user_ex =UserEx.objects.get(id=user.id)
            cart_item, created = Cart.objects.get_or_create(
                user=user_ex,
                product=product_item,
                defaults={
                    'quantity': 1,
                    'subtotal': product_item.price 
                }
            )
            if not created:
                cart_item.quantity += 1 
                cart_item.subtotal += product_item.price
                cart_item.save()
            return redirect('cart')
        except Product.DoesNotExist:
            return HttpResponse("Product not found", status=404)
    else:
        return HttpResponse("Method not allowed", status=405)

#== wish list count on nav bar of base.html ===
def base(request):
    if request.user.is_authenticated:
        # Get the wishlist count for the logged-in user
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    else:
        wishlist_count = 0
    return render(request, 'base.html', {'wishlist_count': wishlist_count})
