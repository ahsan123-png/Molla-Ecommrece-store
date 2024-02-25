from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request,"dashboard.html")

def adminDashboard(request):
    return render(request,"admin/admindashboard.html")
    
def adminForms(request):
    return render (request,"admin/forms.html")

def adminIcons(request):
    return render (request,"admin/icons.html")

def adminLogin(request):
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