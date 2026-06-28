from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


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

    is_job_owner = user.is_authenticated and job.client == user
    is_pilot = hasattr(user, 'pilot_profile') if user.is_authenticated else False
    has_applied = False
    pilot_app_status = None

    # ใบสมัครนักบินที่คัดเลือก และไฟล์ผลลงานที่ส่งมอบไว้
    accepted_application = job.applications.filter(status='ACCEPTED').first()
    is_accepted_pilot = (accepted_application.pilot == user) if accepted_application and user.is_authenticated else False
    deliverables = accepted_application.deliverables.first() if accepted_application else None

    edit_proposal = False

    if is_pilot:
        exiting_app = job.applications.filter(pilot=user).first()
        if exiting_app:
            has_applied = True
            pilot_app_status = exiting_app

    if request.method == 'POST' and is_pilot and not is_job_owner and job.status == 'PENDING':
        if has_applied:
            form = JobApplicationForm(request.POST, instance=pilot_app_status)
            edit_proposal = True
        else:
            form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            if not has_applied:
                application.job = job
                application.pilot = user
            application.save()
            return redirect('job_detail', pk=job.pk)
    elif is_pilot and not is_job_owner and not has_applied:
        form = JobApplicationForm()
    elif is_pilot and not is_job_owner and has_applied and request.GET.get('edit') == '1':
        form = JobApplicationForm(instance=pilot_app_status)
        edit_proposal = True
    else:
        form = None

    # เรียกใช้งานฟอร์มสำหรับการส่งมอบงาน
    deliverable_form = JobDeliverableForm()
    applications = job.applications.all().order_by('-applied_at')

    context = {
            'job': job,
            'form': form,
            'deliverable_form': deliverable_form,
            'is_pilot': is_pilot,
            'is_job_owner': is_job_owner,
            'has_applied': has_applied,
            'edit_proposal': edit_proposal,
            'pilot_app_status': pilot_app_status,
            'applications': applications,
            'accepted_application': accepted_application,
            'is_accepted_pilot': is_accepted_pilot,
            'deliverables': deliverables,
        }
    return render(request, 'app_boarding/job_detail.html', context)


# [นักบินกด] เปลี่ยนสเตตัสเป็น กำลังดำเนินการบิน (IN_PROGRESS)
@login_required
def start_job_view(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    accepted_app = job.applications.filter(status='ACCEPTED').first()

    if accepted_app and accepted_app.pilot == request.user and job.status == 'MATCHED':
        job.status = 'IN_PROGRESS'
        job.save()
    return redirect('job_detail', pk=job.pk)
# [นักบินกด] ฟังก์ชันรับข้อมูลลิงก์ส่งมอบผลงาน
@login_required
def submit_deliverable_view(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    accepted_app = job.applications.filter(status='ACCEPTED').first()
    
    if accepted_app and accepted_app.pilot == request.user and job.status == 'IN_PROGRESS':
        if request.method == 'POST':
            form = JobDeliverableForm(request.POST)
            if form.is_valid():
                accepted_app.deliverables.all().delete() # ลบของเก่าออกถ้ากดส่งอัปเดตใหม่
                deliverable = form.save(commit=False)
                deliverable.application = accepted_app
                deliverable.save()
    return redirect('job_detail', pk=job.pk)
# [ผู้จ้างกด] ตรวจไฟล์งานเสร็จเรียบร้อย เปลี่ยนสเตตัสเป็น เสร็จสิ้น (COMPLETED)
@login_required
def complete_job_view(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    if job.client == request.user and job.status == 'IN_PROGRESS':
        job.status = 'COMPLETED'
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
    
    return render(request, 'app_boarding/job_form.html', {'form': form})

@login_required
def job_edit_view(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    if job.client != request.user or job.status != 'PENDING':
        return redirect('job_detail', pk=job.pk)

    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobPostingForm(instance=job)

    return render(request, 'app_boarding/job_form.html', {
        'form': form,
        'job': job,
        'is_edit': True,
    })

@login_required
def job_delete_view(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    if job.client != request.user or job.status != 'PENDING':
        return redirect('job_detail', pk=job.pk)

    if request.method == 'POST':
        job.delete()
        return redirect('job_list')

    return redirect('job_detail', pk=job.pk)

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