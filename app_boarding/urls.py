from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list_view, name='job_list'),
    path('<int:pk>/', views.job_detail_view, name='job_detail'),
    path('create/', views.job_create_view, name='job_create'),

    # ลงทะเบียนเส้นทางสำหรับรับคำสั่งอนุมัติงาน
    path('accept/<int:app_id>/accept/', views.accept_application_view, name='accept_application'),
]