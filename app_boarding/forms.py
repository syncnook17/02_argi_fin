from django import forms
from django.contrib.gis import forms as gis_forms
from .models import JobCategory, JobPosting, JobApplication

class JobPostingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = None

    class Meta:
        model = JobPosting
        fields = ['category', 'title', 'description', 
                'budget_min', 'budget_max', 'address_text', 
                'deadline', 'start_date', 'location']
        widgets = {
                'category': forms.Select(attrs={'class': 'form-select'}),
                'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'เช่น จ้างพ่นยาโดรนเกษตร ไร่ข้าวเสนา'}),
                'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
                'budget_min': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'งบขั้นต่ำ'}),
                'budget_max': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'งบสูงสุด'}),
                'address_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'อ.เมือง จ.เชียงใหม่'}),
                'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
                
                'location': forms.HiddenInput(attrs={'id': 'id_location'}),
        }


# ฟอร์มสำหรับกรอกเสนอราคาและนัดหมาย
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['bid_price', 'available_dates']
        widgets = {
            'bid_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ราคาที่เสนอ'}),
            'available_dates': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }