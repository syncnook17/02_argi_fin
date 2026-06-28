from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list_view, name='job_list'),
    path('<int:pk>/', views.job_detail_view, name='job_detail'),
    path('create/', views.job_create_view, name='job_create'),
    path('<int:pk>/edit/', views.job_edit_view, name='job_edit'),
    path('<int:pk>/delete/', views.job_delete_view, name='job_delete'),

    # ลงทะเบียนเส้นทางสำหรับรับคำสั่งอนุมัติงาน
    path('accept/<int:app_id>/accept/', views.accept_application_view, name='accept_application'),

    # สำหรับ Status ของนักบิบน
    path('<int:pk>/start/', views.start_job_view, name='start_job'),
    path('<int:pk>/complete_job/', views.complete_job_view, name='complete_job'),
    path('<int:pk>/deliverable/', views.submit_deliverable_view, name='submit_deliverable'),
]