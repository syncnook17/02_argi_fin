from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "app_core/index.html")


@login_required
def dashboard_view(request):
    # ดังข้อมูลผู้ใช้งานที่ login อยู่
    user = request.user

    context = {
        'user': user,
    }
    return render(request, "app_core/dashboard.html", context)