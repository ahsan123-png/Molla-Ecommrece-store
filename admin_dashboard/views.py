from datetime import date
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from product.models import Inventory, Product, ProductVariant
from order.models import Notification, Order
from django.contrib.auth.decorators import login_required

from users.models import Contact, UserEx
# Create your views here.
def dashboard(request):
    return render(request,"dashboard.html")
# ======== access to dashboard  admin =====
@login_required
def homeDashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if request.user.is_superuser:
        total_sales = Order.objects.count()
        today_date = date.today()
        today_sales = Order.objects.filter(order_date__date=today_date).count()
        total_revenue = Order.objects.aggregate(total_revenue=Sum('whole_total'))['total_revenue']
        today_revenue = Order.objects.filter(order_date__date=today_date).aggregate(today_revenue=Sum('whole_total'))['today_revenue']
        latest_orders = Order.objects.all().order_by('-order_date')[:5]
        customer_ids = [order.customer_id for order in latest_orders]
        customers = UserEx.objects.filter(id__in=customer_ids)
        latest_messages = Contact.objects.order_by('-message_at')[:4]
        #unread and read notifications
        unread_notifications = Notification.objects.filter(type="Order" ,is_read=False)
        notifications_count = unread_notifications.filter(type="Order", is_read=False).count()
        unreadMassageNotifications = Notification.objects.filter(type="MESSAGE", is_read=False)
        massageNotifications = Notification.objects.filter(type="MESSAGE", is_read=False).count()
        print(massageNotifications)
        context = {
            'total_sales': total_sales,
            'today_sales': today_sales,
            'total_revenue': total_revenue,
            'today_revenue': today_revenue,
            "latest_orders" : latest_orders,
            "latest_messages" : latest_messages,
            "customers" : customers,
            'unread_notifications': unread_notifications,
            'notifications_count': notifications_count,
            'unreadMassageNotifications': unreadMassageNotifications,
            'massageNotifications': massageNotifications,
        }
        return render(request, 'admin/homeadmin.html' , context)
    else:
        return redirect("admin_login")
#=== Notifications ====
def mark_notification_as_read(request, notification_id):
    notification = Notification.objects.get(pk=notification_id)
    notification.is_read = True
    notification.save()
    return redirect('home_dashboard')
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
def messages(request):
    contactData=Contact.objects.all()
    conData=[]
    for data in contactData:
        info={
            "name" : data.cusName,
            "email" : data.cusEmail,
            "phone" : data.cusPhone,
            "subject" : data.cusSubject,
            "message" : data.cusMessage,
        }
        conData.append(info)
    context={
        "data" : conData
    }
    return render (request,"admin/contact_messages.html" , context)
# ==== admin charts ========
def inventory(request):
    inventory_data = Inventory.objects.all()
    inventory_items = []
    
    for inventory_item in inventory_data:
        product_data = inventory_item.product
        productVariant=ProductVariant.objects.get(id=product_data.id)
        inventory_items.append({
            'product_id': product_data.id,
            'product_name': product_data.product_name,
            'stock_quantity': inventory_item.stock_quantity,
            'price': product_data.price,
            'brand': product_data.brand, 
            'productType': product_data.productType, 
            'category': product_data.category, 
            'subcategory': product_data.subcategory, 
            'color': productVariant.color, 
            'size': productVariant.size, 
        })
    
    context = {
        'inventory_items': inventory_items,
    }
    return render(request, 'admin/inventory.html', context)
# ===== dashboard tables ======
def orderList(request):
    if request.method == "GET":
        orders = Order.objects.all()
        order_data = []
        for order in orders:
            customer = order.customer
            user_info = UserEx.objects.get(id=customer.id)
            user_email = user_info.email

            order_info = {
                'order_id': order.id,
                'order_date': order.order_date,
                'ordered_product_id': order.ordered_product.id,
                'customer_email': user_email,
                'quantity': order.quantity,
                'color': order.color,
                'size': order.size,
                'product_total': order.subtotal,
                'total_bill': order.whole_total
            }
            order_data.append(order_info)
        context = {
            "order_data": order_data
        }
        return render(request, "admin/table.html", context)
# ======= products and order counts ========
@csrf_exempt
def productCounts(request):
    if request.method == "GET":
        pass
# ========= admin base ==========
@login_required
def adminBase(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if request.user.is_superuser:
        total_sales = Order.objects.count()
        today_date = date.today()
        today_sales = Order.objects.filter(order_date__date=today_date).count()
        total_revenue = Order.objects.aggregate(total_revenue=Sum('whole_total'))['total_revenue']
        today_revenue = Order.objects.filter(order_date__date=today_date).aggregate(today_revenue=Sum('whole_total'))['today_revenue']
        latest_orders = Order.objects.all().order_by('-order_date')[:5]
        customer_ids = [order.customer_id for order in latest_orders]
        customers = UserEx.objects.filter(id__in=customer_ids)

        #unread and read notifications
        unread_notifications = Notification.objects.filter(is_read=False)
        notifications_count = unread_notifications.count()
        context = {
            'total_sales': total_sales,
            'today_sales': today_sales,
            'total_revenue': total_revenue,
            'today_revenue': today_revenue,
            "latest_orders" : latest_orders,
            "customers" : customers,
            'unread_notifications': unread_notifications,
            'notifications_count': notifications_count,
        }
        return render(request, 'admin/adminbase.html' , context)
    else:
        return redirect("admin_login")
