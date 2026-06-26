from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PilotRegistrationForm
from app_boarding.models import JobPosting, JobApplication

# Create your views here.
def index(request):
    return render(request, "app_core/index.html")


@login_required
def dashboard_view(request):
    
    # ดังข้อมูลผู้ใช้งานที่ login อยู่
    user = request.user
    # ตรวจสอบว่าผู้ใช้เป็นนักบินโดรนหรือไม่
    is_pilot = hasattr(user, 'pilot_profile')
    # ดึงข้อมูลงานที่ผู้ใช้งานคนนี้เป็นคน "ลงประกาศ" (ฝั่งผู้จ้าง)
    my_jobs = JobPosting.objects.filter(client=user).order_by('-created_at')
    # ดึงประวัติการยื่นเสนอราคา/รับงาน (ฝั่งนักบิน) เก็บทุกสถานะ
    my_applications = None
    if is_pilot:
        my_applications = JobApplication.objects.filter(pilot=user).order_by('-applied_at')


    context = {
        'user': user,
        'is_pilot': is_pilot,
        'my_jobs': my_jobs,
        'my_applications': my_applications,
    }
    return render(request, "app_core/dashboard.html", context)

@login_required
def pilot_registration_view(request):
    # ถ้าลงทะเบียนไว้แล้วให้กลับไปที่หน้าแดชบอร์ด
    if hasattr(request.user, 'pilot_profile'):
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PilotRegistrationForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('dashboard')
    else:
        form = PilotRegistrationForm()
    
    return render(request, "app_core/pilot_register_form.html", {'form': form})

def landing_page_view(request):
    return render(request, "app_core/landing_page.html")