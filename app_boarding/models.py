from django.contrib.gis.db import models 
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your models here.

class JobCategory(models.Model):
    GEOM_CHOICES = [
        ('poing', 'Point (ตำแหน่งการถ่ายภาพ)'),
        ('line', 'Line (ถ่ายวิดีโอเส้นทาง)'),
        ('polygon', 'Polygon (ทำแผนที่ / โดรนเกษตร)'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    geom_type = models.CharField(max_length=50, choices=GEOM_CHOICES)
    icon = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name

class JobPosting(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'เปิดรับสมัคร'),
        ('MATCHED', 'จับคู่สำเร็จ'),
        ('IN_PROGRESS', 'กำลังดำเนินการ'),
        ('COMPLETED', 'เสร็จสิ้น'),
        ('CANCELED', 'ยกเลิก'),
    ]
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_created')
    category = models.ForeignKey(JobCategory, on_delete=models.PROTECT, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget_min = models.DecimalField(max_digits=10, decimal_places=2)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2)

    location = models.GeometryField(srid=4326)
    address_text = models.CharField(max_length=255)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
    deadline = models.DateField(help_text="เดดไลน์การเปิดรับสมัคร")
    start_date = models.DateTimeField(help_text="วันเวลานัดหมายเริ่มบิน")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title


# เก็บข้อมูลนักบินโดรนที่เสนอราคาและนัดหมาย
class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'รอการตอบรับ'),
        ('ACCEPTED', 'ผ่านการคัดเลือก'),
        ('REJECTED', 'ปฏิเสธการคัดเลือก'),
    ]
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    pilot = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    bid_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ราคาที่เสนอ')
    available_dates = models.DateField(help_text='วันที่ที่สามารถทำงานได้')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['job', 'pilot']

    def __str__(self):
        return f"งาน: {self.job.title} - นักบิน: {self.pilot.username} ({self.bid_price})"



