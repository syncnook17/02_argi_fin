from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import JobCategory, JobPosting
from .forms import JobPostingForm


# Create your views here.
# 1. หน้าแสดงประกาศงานทั้งหมด
def job_list_view(request):
    # ดึงงานที่ยังเปิดรับอยู่มาแสดงทั้งหมด
    jobs = JobPosting.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'app_boarding/job_list.html', {'jobs':jobs})

# 2.หน้าสำหรับรายละเอียดงานแต่ละชิ้น
def job_detail_view(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    return render(request, 'app_boarding/job_detail.html', {'job':job})

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