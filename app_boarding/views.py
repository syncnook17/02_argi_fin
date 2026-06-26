from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import JobCategory, JobPosting, JobApplication
from .forms import JobPostingForm, JobApplicationForm


# Create your views here.
# 1. หน้าแสดงประกาศงานทั้งหมด
def job_list_view(request):
    # ดึงงานที่ยังเปิดรับอยู่มาแสดงทั้งหมด
    jobs = JobPosting.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'app_boarding/job_list.html', {'jobs':jobs})

# 2.หน้าสำหรับรายละเอียดงานแต่ละชิ้น
def job_detail_view(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    user = request.user

    # ข้อมูลเริ่มต้น
    is_pilot = hasattr(user, 'pilot_profile') if user.is_authenticated else False
    has_applied = False
    pilot_app_status = None

    # ตรวจสอบว่านักบินเคยเสนอราคาหรือไม่
    if is_pilot:
        exiting_app = JobApplication.objects.filter(job=job, pilot=user).first()
        if exiting_app:
            has_applied = True
            pilot_app_status = exiting_app
    
    # จัดการกรณีที่นักบินกดยื่นเสนอราคา
    if request.method == 'POST' and is_pilot and not has_applied:
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.pilot = user
            application.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobApplicationForm()
    
    # ดึงรายชื่อนักบินที่มาสมัครทั้งหมด (สำหรับให้ผู้จ้างงานดู)
    applications = job.applications.all().order_by('-applied_at')

    context = {
        'job': job,
        'form': form,
        'is_pilot': is_pilot,
        'has_applied': has_applied,
        'pilot_app_status': pilot_app_status,
        'applications': applications,
    }
    return render(request, 'app_boarding/job_detail.html', context)

# ป้องกันไม่ให้คนอื่นมาแอบกดอนุมัติงานแทนเจ้าของงานตัวจริง
@login_required
def accept_application_view(request, app_id):
    application = get_object_or_404(JobApplication, pk=app_id)
    job = application.job

    # ป้องกันไม่ให้คนอื่นมาแอบกดอนุมัติงานแทนเจ้าของงานตัวจริง
    if job.client != request.user:
        return redirect('job_detail', pk=job.pk)
    
    # อัปเดตสถานะใบสมัครนี้ผ่านการคัดเลือก
    application.status = 'ACCEPTED'
    application.save()

    # อัปเดตใบสมัครอื่นๆ ให้สถานะเป็นปฏิเสธ
    job.applications.exclude(pk=app_id).update(status='REJECTED')

    # ปรับสถานะงานให้เป็น จับคู่สำเสร็จเพื่อเริมงาน
    job.status = 'MATCHED'
    job.save()

    return redirect('job_detail', pk=job.pk)

# 3.หน้าฟอร์มสำหรับการลงประกาศงานใหม่
@login_required
def job_create_view(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.client = request.user       # ผูกงานนี้เข้ากับผู้จ้างที่ล็อกอินอยู่
            job.save()
            return redirect('job_list')
    else:
        form = JobPostingForm()
    
    return render(request, 'app_boarding/job_form.html', {'form':form})