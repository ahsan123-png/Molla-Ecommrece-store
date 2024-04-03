import json
from datetime import datetime
from django.core.paginator import Paginator
from order.models import Notification
from product.models import Product , ProductPicture
from product.serializers import ProductPictureSerializer,ProductSerializer
from typing import Any
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.hashers import check_password
#======== models & serializer =========
from .models import Contact, UserEx
from .serializers import UserSerializer
# =======================================
def home(request):
    try:
        product_data = []
        products = Product.objects.all()
        paginator = Paginator(products, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if not products:
            return render(
                request, 
                "index-5.html",
                {
                    "error": "No products available"
                }
            )
        for product in page_obj:
            product_serializer = ProductSerializer(product, context={"request": request}).data
            product_pictures = ProductPicture.objects.filter(product=product)
            product_serializer['product_pictures'] = product_pictures
            product_data.append(product_serializer)
        return render(
            request, 
            "index-5.html",
            {
                "product_data": product_data,
                "page_obj": page_obj
            }
        )
    except Exception as e:
        return render(
            request, 
            "list-products.html",
            {
                "error": f"Internal Server Error: {e}"
            },
            status=500
        )
    
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
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in
            login(request, user)
            return redirect("home")
        else:
            return JsonResponse({"error": "Unable to log in the user"}, status=500)
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
        return redirect('/signin')
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
    if request.method == "POST":
        try:
            user = UserEx.objects.get(id=id)
            # previous_data = UserSerializer(user, context={'request': request}).data
            # Update user fields from form data
            if 'name' in request.POST:
                user.name = request.POST['name']
            if 'email' in request.POST:
                user.email = request.POST['email']
            if 'address' in request.POST:
                user.useraddress = request.POST['address']
            # Save updated user data
            user.save()
            return redirect('profile')
            # new_data = UserSerializer(user, context={'request': request}).data
            # return JsonResponse({
            #     'previous_data': previous_data,
            #     'new_data': new_data,
            # })
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
def about(request):
    return render(request,"about.html")

def contact(request):
    if request.method == "POST":
        name=request.POST.get("name")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        subject=request.POST.get("subject")
        message=request.POST.get("message")
        userContact=Contact.objects.create(
            cusName=name,
            cusEmail=email,
            cusPhone=phone,
            cusSubject=subject,
            cusMessage=message
        )
        userContact.save()
        Notification.objects.create(
            message=f'New contact message from {name}: {message}',
            type='MESSAGE',
            created_at=datetime.now(),
            is_read=False
        )
    return render(request,"contact.html")

def faq(request):
    return render(request,"faq.html")

def coming_soon(request):
    return render(request , "coming-soon.html")

def profile(request):
    user = UserEx.objects.get(id=request.user.id)  # Assuming you have a logged-in user
    return render(request, 'profile.html', {'user': user})

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