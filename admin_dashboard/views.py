from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def dashboard(request):
    return render(request,"dashboard.html")

def adminDashboard(request):
    return render(request,"admin/admindashboard.html")
    
def adminForms(request):
    return render (request,"admin/forms.html")

def adminIcons(request):
    return render (request,"admin/icons.html")
@csrf_exempt
def adminLogin(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username ,password=password)
        if not user.is_superuser:
            return redirect("adminLogin")
        if user is not None:
            login(request,user)
            return redirect("adminDashboard")
    return render (request,"admin/login.html")

def adminProfile(request):
    return render (request,"admin/profile.html")

def adminRegister(request):
    
    return render (request,"admin/register.html")

def adminResetPassword(request):
    return render (request,"admin/reset-password.html")

def adminTables(request):
    return render (request,"admin/tables.html")

def adminCalender(request):
    return render (request,"admin/calendar.html")

def adminBase(request):
    return render (request,"admin/adminbase.html")