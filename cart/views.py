from django.shortcuts import redirect, render
# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from product.models import Product
from users.models import UserEx
from .models import Cart, Wishlist
from django.views.decorators.csrf import csrf_exempt
from users.views import getUserEx
# ==========================================
def cart(request):
    if request.method == "GET":
        cart_data = []
        user = request.user
        initial_subtotal = 0 
        if isinstance(user, UserEx):
            cart_items = Cart.objects.filter(user=user)
        else:
            cart_items = Cart.objects.filter(user=user)
        for item in cart_items:
            product = item.product
            cart_item_data = {
                'product_name': product.product_name,
                'price': product.price,
                'quantity': item.quantity,
                'product_total': item.subtotal * item.quantity,
                'total': item.subtotal,
                'product_id': product.id,
                'image': None 
            }
            if product.pictures.exists():
                cart_item_data['image'] = product.pictures.first().picture.url
            cart_data.append(cart_item_data)
            initial_subtotal += item.subtotal
    return render(request, 'cart.html', {'cart_data': cart_data,"initial_subtotal" :initial_subtotal })
# ==== add items to wishlist page =====
@csrf_exempt
def addToWishlist(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('signin')
        user = request.user
        user_ex=getUserEx(user)
        if not user_ex:
            return redirect('userNotFound')
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
            'product_id': product.id,
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
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('signin')
        try:
            product_item = Product.objects.get(id=id)
            user = request.user
            user_ex=getUserEx(user)
            if not user_ex:
                return redirect("userNotFound")
            selected_color = request.POST.get('color_select')
            selected_size = request.POST.get('size')
            print(selected_color , selected_size)

            cart_item, created = Cart.objects.get_or_create(
                user=user_ex,
                product=product_item,
                defaults={
                    'quantity': 1,
                    'subtotal': product_item.price,
                    'selected_color': selected_color,
                    'selected_size': selected_size
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

# ==== delete product from cart ====
@csrf_exempt
def removeFromCart(request, id):
    if request.method == "DELETE":
        cart_item = get_object_or_404(Cart, product_id=id)
        cart_item.delete()
        return JsonResponse({'message': 'Item removed from cart.'})
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)
    
# === remove product from wishlist =====
@csrf_exempt
def removeFromWishlist(request, id):
    if request.method == "DELETE":
        wishlist_item = get_object_or_404(Wishlist, product_id=id)
        wishlist_item.delete()
        return JsonResponse({'message': 'Product removed successfully from wishlist'}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

    