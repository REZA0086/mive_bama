from django.db import models
from account.models import *
# Create your models here.

class Article(models.Model):
    image = models.ImageField(upload_to="images/",verbose_name="عکس مقاله")
    title = models.CharField(max_length=250,verbose_name="عنوان مقاله")
    author = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True,verbose_name="نویسنده مقاله")
    description = models.TextField(verbose_name="متن مقاله")

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

