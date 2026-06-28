from django import forms
from .models import PilotProfile
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()

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


# ฟอร์มสำหรับสมัครสมาชิกใหม่
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'อีเมล'})
    )
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # วนลูปสวมคลาส form-control ของ Bootstrap ให้กับทุกฟิลด์อัตโนมัติ
        for field in self.fields:
            if field != 'email':
                self.fields[field].widget.attrs.update({'class': 'form-control'})