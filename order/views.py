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

        # Fetch the cart items for the logged-in user
        cart_items = Cart.objects.filter(user=user)

        # Create an Order object for each cart item
        for cart_item in cart_items:
            order = Order.objects.create(
                customer=user,
                product=cart_item.product,
                subtotal=cart_item.subtotal,  # Assuming total_price is a field in your Cart model
                color=cart_item.color,
                size=cart_item.size,
                quantity=cart_item.quantity,
                first_name=cart_item.first_name,
                last_name=cart_item.last_name,
                email=cart_item.email,
                phone=cart_item.phone,
                additional_note=cart_item.additional_note
                # Add more fields as needed
            )
            order.save()

        # Delete all cart items associated with the user
        cart_items.delete()
    return render(request, 'checkout.html', {'initial_subtotal': initial_subtotal})

def shipment_address(request):
    return render(request,"checkout.html")