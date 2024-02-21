from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request,"dashboard.html")

def adminDashboard(request):
    return render(request,"admin/admin-dashboard.html")