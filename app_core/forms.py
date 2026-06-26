from django import forms
from .models import PilotProfile

# ฟอร์มสำหรับลงทะเบียนเป็นนักบินโดรน
class PilotRegistrationForm(forms.ModelForm):
    class Meta:
        model = PilotProfile
        fields = ['lic_num', 'phone', 'drone_model']
        widgets = {
            'lic_num': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'เลขที่ใบอนุญาต'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'หมายเลขโทรศัพท์'}),
            'drone_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'รุ่นโดรน'}),
        }
