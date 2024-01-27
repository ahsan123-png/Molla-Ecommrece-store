from django.shortcuts import render

def home(request):

    
    return render(request, "index-5.html")



def signin(request):
    return render(request,"login.html")


def register(request):
    return render(request,"login.html")


def blog(request):
    return render(request , "blog.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def faq(request):
    return render(request,"faq.html")

def coming_soon(request):
    return render(request , "coming-soon.html")
