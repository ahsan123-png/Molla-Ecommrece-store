from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from .models import UserEx
from django.contrib import messages
def home(request):
    return render(request, "index-5.html")
#==== register user ====
@csrf_exempt
def register(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get("password")
        username = email.split('@')[0]
        if UserEx.objects.filter(email=email).exists() or UserEx.objects.filter(phone=phone).exists():
            return JsonResponse({"error": "User with provided email or phone already exists"}, status=400)
        user = UserEx.objects.create_user(phone=phone, email=email, password=password, username=username)
        user.set_password(password)
        user.set_customer_id()
        user.save()
        return redirect("home")
    else:
        # Handle unsupported HTTP methods
        return JsonResponse({"error": f"Method {request.method} is not supported"}, status=405)

#==== Signin user ====
@csrf_exempt
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = email.split('@')[0]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
            return redirect('about')
    return render(request, 'login.html')

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
