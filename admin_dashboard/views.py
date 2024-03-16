from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from product.models import Product
from order.models import Order
from django.contrib.auth.decorators import login_required
# Create your views here.
def dashboard(request):
    return render(request,"dashboard.html")
# ======== access to dashboard  admin =====
@login_required
def homeDashboard(request):
    if not request.user.is_authenticated:
        return redirect('adminLogin')
    else:
        return render(request, 'admin/homeadmin.html')
# ====== login admin ========= 
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
    return render (request,"admin/signin.html")
# ==== admin registeration ========
def adminRegister(request):
    return render (request,"admin/signup.html")
# ==== admin forms ========
def adminForms(request):
    return render (request,"admin/form.html")
# ==== admin charts ========
def adminChart(request):
    return render (request,"admin/chart.html")
# ===== dashboard tables ======
def adminTables(request):
    return render (request,"admin/table.html")
# ======= products and order counts ========
@csrf_exempt
def productCounts(request):
    if request.method == "GET":
        pass

