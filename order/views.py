from django.shortcuts import render
import ast

def checkout(request):
    if request.method == "GET":
        cart_data_encoded = request.GET.get('cart_data')
        initial_subtotal = request.GET.get('initial_subtotal', None)
        cart_data_encoded = cart_data_encoded.replace("Decimal", "").replace("(", "").replace(")", "")
        print("Encoded Cart Data:", cart_data_encoded)
        if cart_data_encoded:
            try:
                cart_data = ast.literal_eval(cart_data_encoded)
            except ValueError as e:
                print(f"Error decoding JSON data: {e}")
                cart_data = None
            else:
                print("Decoded Cart Data:", cart_data)  # Debug print
        return render(request, 'checkout.html', {'cart_data': cart_data, 'initial_subtotal': initial_subtotal})



def shipment_address(request):
    return render(request,"checkout.html")