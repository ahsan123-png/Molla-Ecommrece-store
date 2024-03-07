import json
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import ast
from django.views.decorators.csrf import csrf_exempt
from cart.models import Cart
from order.models import Order, ShipmentAddress
from product.models import Product
from users.models import UserEx
from django.contrib.auth.decorators import login_required
#=================== views here ===================
@login_required
def checkout(request):
    if request.method == "GET":
        color = []
        size = []
        product_ids = []
        cart_data = json.loads(request.GET.get('cart_data', '[]'))
        initial_subtotal = float(request.GET.get('initial_subtotal', 0))
        user = request.user
        if isinstance(user, UserEx):
            user_ex = user
        else:
            user_ex = UserEx.objects.get(id=user.id)
        cart_items = Cart.objects.filter(user=user_ex)
        for i in cart_items:
            product_ids.append(i.product.id)
            color.append(i.selected_color)
            size.append(i.selected_size)
        for item,product_id, c, s in zip(cart_data,product_ids ,color, size):
            product = get_object_or_404(Product, id=product_id)
            order = Order.objects.create(
                customer=user_ex,
                ordered_product=product,
                subtotal=item['total'],
                quantity=item['quantity'],
                whole_total=initial_subtotal,
                color=c,
                size=s
                # Add other fields as needed
            )
            order.save()
        cart_items.delete()
        try:
            last_order = Order.objects.filter(customer=user_ex).latest('order_date')
        except Order.DoesNotExist:
            raise Http404("No matching Order found")
        return render(request, 'checkout.html', {'initial_subtotal': initial_subtotal, 'order': last_order})
    else:
        return HttpResponseBadRequest("Invalid request method")
@csrf_exempt
def shipmentAddress(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        street_address_one = request.POST.get('street_address_one')
        street_address_two = request.POST.get('street_address_two')
        street_address = street_address_one + street_address_two
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        phone_number = request.POST.get('phone_number')
        additional_note = request.POST.get('additional_note')
        order_id = request.POST.get('order_id')
        paymentMethod=request.POST.get("payment_method")
        user = request.user
        if isinstance(user, UserEx):
            user_ex = user
        else:
            user_ex = UserEx.objects.get(id=user.id)
        shipment_address = ShipmentAddress.objects.create(
            order=order,
            customer=user_ex,
            first_name=first_name,
            last_name=last_name,
            email=email,
            street_address=street_address,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            phone_number=phone_number,
            additional_note=additional_note,
            payment_method=paymentMethod
        )
        shipment_address.save()
        return redirect('home')  # Redirect to the checkout page or any other page
    return render(request, "checkout.html")
"""shipment_address.orders.set(orders) is a Django ORM method used to set the related orders for a ShipmentAddress instance. It takes an iterable of Order instances (in this case, the variable orders) and associates them with the ShipmentAddress.

In other words, when you call set(orders), it replaces any existing set of orders for that ShipmentAddress with the new set provided. This is useful when you want to update the associated orders for a ShipmentAddress.
It creates a new ShipmentAddress instance and associates it with the orders specified in the orders variable. This ensures that this shipment address is linked to those specific orders.

After this operation, if you access shipment_address.orders.all(), you'll get the set of orders associated with that ShipmentAddress.


this is the Query to get the all order of a user from shipment address

shipment_address = ShipmentAddress.objects.get(id=your_shipment_address_id)
orders = shipment_address.orders.all()
"""