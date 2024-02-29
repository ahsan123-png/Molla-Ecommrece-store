from django.shortcuts import redirect, render
import ast
from django.views.decorators.csrf import csrf_exempt
from cart.models import Cart
from order.models import Order, ShipmentAddress
from users.models import UserEx
from django.contrib.auth.decorators import login_required
#=================== views here ===================
@login_required
def checkout(request):
    initial_subtotal = None  # Default value
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

@csrf_exempt
def shipmentAddress(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        street_address_one=request.POST.get('street_address_one')
        street_address_two=request.POST.get('street_address_two')
        street_address =street_address_one + street_address_two
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        phone_number = request.POST.get('phone_number')
        additional_note = request.POST.get('additional_note')
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        shipment_address = ShipmentAddress.objects.create(
            order=order,
            customer=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            street_address=street_address,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            phone_number=phone_number,
            additional_note=additional_note
        )
        shipment_address.save()
        return redirect('home')  # Redirect to the checkout page or any other page
    return render(request,"checkout.html")