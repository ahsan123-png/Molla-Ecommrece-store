from django.shortcuts import render

# Create your views here.


def cart(request):
    return render(request,"cart.html")


def wishlist(request):
    return render(request,"wishlist.html")

