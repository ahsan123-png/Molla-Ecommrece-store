from django.shortcuts import render

# Create your views here.

def blog(request):
    return render(request , "blog.html")

def review(request):
    return render(request,"single.html")

