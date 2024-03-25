from datetime import date
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from product.models import Product
from order.models import Order
from django.contrib.auth.decorators import login_required

from users.models import UserEx
# Create your views here.
def dashboard(request):
    return render(request,"dashboard.html")
# ======== access to dashboard  admin =====
@login_required
def homeDashboard(request):
    if not request.user.is_authenticated:
        return redirect('adminLogin')
    if request.user.is_superuser:
        total_sales = Order.objects.count()
        today_date = date.today()
        today_sales = Order.objects.filter(order_date__date=today_date).count()
        total_revenue = Order.objects.aggregate(total_revenue=Sum('whole_total'))['total_revenue']
        today_revenue = Order.objects.filter(order_date__date=today_date).aggregate(today_revenue=Sum('whole_total'))['today_revenue']
        latest_orders = Order.objects.all().order_by('-order_date')[:5]
        customer_ids = [order.customer_id for order in latest_orders]
        customers = UserEx.objects.filter(id__in=customer_ids)
        context = {
            'total_sales': total_sales,
            'today_sales': today_sales,
            'total_revenue': total_revenue,
            'today_revenue': today_revenue,
            "latest_orders" : latest_orders,
            "customers" : customers
        }
        return render(request, 'admin/homeadmin.html' , context)
    else:
        return redirect("adminLogin")
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
            return redirect("home_dashboard")
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

