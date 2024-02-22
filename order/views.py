import json
from django.shortcuts import render
from django.http import QueryDict
from urllib.parse import unquote

def checkout(request):
    if request.method == "GET":
        # import pdb;pdb.set_trace()
        cart_data = request.GET.get('cart_data', None)
        initial_subtotal = request.GET.get('initial_subtotal', None)
        if cart_data:
            cart_data = unquote(cart_data)
            # cart_data = QueryDict(cart_data)
            cart_data = json.loads(cart_data)

        return render(request, 'checkout.html', {'cart_data': cart_data, 'initial_subtotal': initial_subtotal})

def shipment_address(request):
    return render(request,"checkout.html")