from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    avatar = models.CharField( max_length=20,verbose_name='تصویر آواتار',blank=True,null=True)
    email_active_code = models.CharField(max_length=100,verbose_name="کد فعالسازی ایمیل")
    confirm_password = models.CharField(max_length=100,verbose_name="تکرار کلمه عبور",null=True,blank=True)

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.username