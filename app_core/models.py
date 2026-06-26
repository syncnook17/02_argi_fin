from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

# สำหรับลงทะเบียนเป็นนักบินโดรน
User = get_user_model()
class PilotProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pilot_profile')
    lic_num = models.CharField(max_length=20, unique=True, verbose_name='เลขที่ใบอนุญาต')
    phone = models.CharField(max_length=10, verbose_name='หมายเลขโทรศัพท์')
    drone_model = models.CharField(max_length=255, verbose_name='รุ่นโดรน')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"นักบิน: {self.user.username} ({self.lic_num})"
