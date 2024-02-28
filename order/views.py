from django.shortcuts import render
import ast
from cart.models import Cart
from order.models import Order
from users.models import UserEx
from django.contrib.auth.decorators import login_required
#=================== views here ===================
@login_required
def checkout(request):
    if request.method == "GET":
        initial_subtotal = request.GET.get('initial_subtotal', None)
        user = request.user
        if isinstance(user, UserEx):
            user_ex = user
        else:
            user_ex = UserEx.objects.get(id=user.id)
        cart_items = Cart.objects.filter(user=user_ex)
        for cart_item in cart_items:
            order = Order.objects.create(
                customer=user_ex,
                ordered_product=cart_item.product,
                subtotal=cart_item.subtotal,
                color=cart_item.selected_color,
                size=cart_item.selected_size,
                quantity=cart_item.quantity,
            )
            order.save()
        cart_items.delete()
    return render(request, 'checkout.html', {'initial_subtotal': initial_subtotal})

def shipment_address(request):
    return render(request,"checkout.html")