from django.shortcuts import render

# Create your views here.
def chcekout(request):
    return render(request,"checkout.html")

def shipment_address(request):
    return render(request,"checkout.html")