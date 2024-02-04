import json
from typing import Any
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.hashers import check_password
#======== models & serializer =========
from .models import UserEx
from .serializers import UserSerializer
# =======================================
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
# ======== logged out ================
def logout_view(request):
    if request.method=='GET':
        messages.info(request,"Logged out successfully!")
        logout(request)
        return redirect('login')
# ========== CUARD Users =============
# ------>>>>>>> Loading >>>>>>
# ====== Get all Users =======
@csrf_exempt
def all_users(request):
    if request.method == "GET":
        try:
            users=UserEx.objects.all()
            if users is None:
                return bad_response(
                    request.method,{
                        f"No user available"
                    },status=404
                )
            user_details = []
            for user in users:
                user_data = UserSerializer(user, context={"request": request}).data
                user_details.append(user_data)

            return JsonResponse({
                "success": "Retrieved all users successfully",
                "users": user_details
            },status=200)
        except Exception as e:
            return bad_response(
                request.method,{
                    "error" : f"Internal server Error {e}"
                },status=500
            )
    else:
        return JsonResponse(bad_response(
            request.method,
            f"Method {request.method} Not Allowed"
        ))
#======== get user by id ===========
def get_user(request,id):
    if request.method == "GET":
        try:
            user=UserEx.objects.get(id = id)
            if user is None:
                return bad_response(
                    request.method,{
                        "error" : f"User with id {id} Doesn't Exits"
                    },status=404
                )
            user_serializer=UserSerializer(user,context={"request" : request}).data
            return good_response(
                request.method,{
                    "success" : user_serializer
                },status=200
            )
        except Exception as e:
            return bad_response(
                request.method,{
                    "error" : f"Internal server error {e}"
                },status=500
            )
    else:
        return bad_response(
            request.method,
            f"Method {request.method} Not Allowed"
        )
# ======= update a user by id =========
@csrf_exempt
def update(request, id):
    if request.method == "PUT":
        req_data = json.loads(request.body)
        try:
            user = UserEx.objects.get(id=id)
            previous_data = UserSerializer(user, context={'request': request}).data

            # Check password if provided
            password = req_data.get('password')
            if password and not check_password(password, user.password):
                return JsonResponse({'error': 'Incorrect password'}, status=400)

            # Update user fields if provided
            if 'name' in req_data:
                user.name = req_data['name']
            if 'email' in req_data:
                user.email = req_data['email']
            if 'address' in req_data:
                user.address = req_data['address']
            if 'device_id' in req_data:
                user.device_id = req_data['device_id']

            # Update password if new password provided
            new_password = req_data.get('new_password')
            if new_password:
                user.set_password(new_password)

            user.save()
            new_data = UserSerializer(user, context={'request': request}).data
            return JsonResponse({
                'previous_data': previous_data,
                'new_data': new_data,
            })

        except UserEx.DoesNotExist:
            return JsonResponse({'error': f'User with id {id} does not exist'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': f"Method {request.method} Not Allowed"}, status=405)
# ======= delete a user by id =========
def delete(request,id):
    pass
# ====================================
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

def profile(request):
    return render (request , "profile.html")

#======= some usefull functions ============
def get_request_body(request):
    return json.loads(request.body)


def good_response(method: str, data: dict | Any, status: int = 200):
    return JsonResponse({
        "success": True,
        "data": data,
        "method": method,
        "status": status,
    })


def bad_response(method: str, reason: str, status: int = 403, data: dict | Any = None):
    return JsonResponse({
        "success": False,
        "reason": reason,
        "data": data,
        "status": status,
        "method": method,
    })