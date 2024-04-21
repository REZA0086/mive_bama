from django import forms
from django.core.exceptions import ValidationError
from .models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "نام خود را وارد کنید"}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "آدرس ایمیل خود را وارد کنید"}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "پسورد خود را وارد کنید"}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "پسورد خود دوباره را وارد کنید"}),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password
        else:
            raise ValidationError("کلمه عبور و تکرار آن یکی نیستند")


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "آدرس ایمیل خود را وارد کنید"}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "پسورد خود را وارد کنید"}),
        }


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "آدرس ایمیل خود را وارد کنید"}))


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "پسورد خود را وارد کنید"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "پسورد خود دوباره را وارد کنید"}))



