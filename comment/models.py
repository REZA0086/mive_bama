from django.db import models
from account.models import *
from blog.models import Product


# Create your models here.

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True,verbose_name="کامنت محصول")
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="نویسنده کامنت")
    description = models.TextField(verbose_name="متن کامنت")
    is_active = models.BooleanField(default=True, verbose_name="تایید شده/ نشده")

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

class Response_Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="نویسنده پاسخ کامنت")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,verbose_name="کامنت پاسخ دهی شده")
    response = models.CharField(max_length=300,verbose_name="متن پاسخ کامنت")
    is_active = models.BooleanField(default=True, verbose_name="تایید شده/ نشده")


    def __str__(self):
        return self.comment.description

    class Meta:
        verbose_name = "جواب کامنت"
        verbose_name_plural = "جواب کامنت ها"