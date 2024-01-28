from typing import Any
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
#======= import models ===========
from .models import UserEx
 
#==============================================
def home(request):
    return render(request, "index-5.html")
#===== Login =====
@csrf_exempt
def signin(request):
    if request.method=="POST":
        email=request.POST["email"]
        password=request.POST["password"]
        user_= authenticate(request, email=email,password=password)
        print(user_)
        if user_ is not None:
            messages.success(request," You are logged in")
            login(request,user_)
            return redirect('home')
        else:
            messages.error(request,"Invalid credentials")
            return redirect('about')
    return render(request,'login.html')

#==== register form =====
@csrf_exempt
def register(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get("password")
        username=email.split('@')[0]
        if UserEx.objects.filter(email=email).exists() or UserEx.objects.filter(phone=phone).exists():
            return JsonResponse({"error": "User with provided email or phone already exists"}, status=400)
        user = UserEx.objects.create_user(phone=phone, email=email, password=password,username=username)
        user.set_password(password)
        user.set_customer_id()
        user.save()
        return redirect("home")
    return render(request , "login.html")
    # else:
    #     # Handle unsupported HTTP methods
    #     return JsonResponse({"error": f"Method {request.method} is not supported"}, status=405)
#========== logout ============
def logout_view(request):
    if request.method=='GET':
        messages.info(request,"Logged out successfully!")
        logout(request)
        return redirect('login')
#======== user CURD =======
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



#============= some useful functions ===========
def good_response(method: str, data: dict | Any, status: int = 200):
    return {
        "success": True,
        "data": data,
        "method": method,
        "status": status,
    }


def bad_response(method: str, reason: str, status: int = 403, data: dict | Any = None):
    return {
        "success": False,
        "reason": reason,
        "data": data,
        "status": status,
        "method": method,
    }


def clean_phone_number(phone_number):
    if phone_number.__contains__("+"):
        phone_number = phone_number.replace("+", "")
    if phone_number.__contains__(" "):
        phone_number = phone_number.replace(" ", "")
    if phone_number.__contains__("-"):
        phone_number = phone_number.replace("-", "")
    return phone_number
