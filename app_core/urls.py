from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),

# ดึง LoginView ของ Django มาใช้งานตรงๆ พร้อมระบุตำแหน่งไฟล์ Template ของเรา
    path('login/', auth_views.LoginView.as_view(template_name='app_core/login.html'), name='login'),
    
    # ดึง LogoutView ของ Django มาจัดการตัด Session
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # หน้าแดชบอร์ดส่วนตัว
    path('dashboard/', views.dashboard_view, name='dashboard'),
]