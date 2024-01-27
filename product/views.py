from django.shortcuts import render

# Create your views here.
def products(request):
    return render(request,"list-products.html")

def product_details(request):
    return render(request,"product-detail.html")

