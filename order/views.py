from django.shortcuts import render
import ast

import ast

import ast

def checkout(request):
    if request.method == "GET":
        initial_subtotal = request.GET.get('initial_subtotal', None)
        return render(request, 'checkout.html', {'initial_subtotal': initial_subtotal})


def shipment_address(request):
    return render(request,"checkout.html")