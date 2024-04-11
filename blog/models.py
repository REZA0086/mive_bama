from account.models import *
from django_jalali.db import models as jmodels
import jdatetime


class Category(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, verbose_name="عکس دسته بندی")
    name = models.CharField(max_length=250, verbose_name="نام دسته بندی")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, verbose_name="دسته بندی")
    image = models.ImageField(upload_to='images/', verbose_name="عکس محصول")
    title = models.CharField(max_length=250, verbose_name="عنوان محصول")
    price = models.DecimalField(max_digits=11, decimal_places=0, verbose_name="قیمت")
    discount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="تخفیف")
    created_time = jmodels.jDateField(null=True, blank=True, verbose_name="تاریخ ثبت محصول",
                                      default=jdatetime.datetime.today())
    order_count = models.IntegerField(default=0, verbose_name="تعداد فروش")

    visited_count = models.IntegerField(default=0, verbose_name="تعداد بازدید")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر امتیاز دهنده")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, verbose_name="امتیاز محصول")
    value = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="مقدار امتیاز")

    class Meta:
        verbose_name = "امتیاز محصول"
        verbose_name_plural = "امتیاز محصولات"


class HeaderIndex(models.Model):
    title = models.CharField(max_length=250, verbose_name="عنوان بالا صفحه")
    logo = models.ImageField(upload_to='images/', verbose_name="لوگو بالا صفحه")

    class Meta:
        verbose_name = "داینامیک هدر صفحه اصلی"
        verbose_name_plural = "داینامیک هدر های صفحه"


class TitleIndex(models.Model):
    image = models.ImageField(upload_to='images/', verbose_name="عکس بالا صفحه اصلی")
    title = models.CharField(max_length=250, verbose_name="عنوان ")
    title1 = models.CharField(max_length=250, verbose_name="عنوان 1")
    title2 = models.CharField(max_length=250, verbose_name="عنوان 2")
    title3 = models.CharField(max_length=250, verbose_name="عنوان 3")
    title4 = models.CharField(max_length=250, verbose_name="عنوان 4")

    class Meta:
        verbose_name = "داینامیک عکس بالای صفحه اصلی"


class SliderIndex(models.Model):
    title = models.CharField(max_length=250, verbose_name="عنوان اسلایدر")
    description = models.TextField(verbose_name="متن اسلایدر")
    image = models.ImageField(upload_to='images/', verbose_name="عکس اسلایدر")

    class Meta:
        verbose_name = "داینامیک اسلایدر صفحه اصلی"
        verbose_name_plural = "داینامیک اسلایدر های صفحه اصلی"

class ImageIndex(models.Model):
    image = models.ImageField(upload_to='images/', verbose_name="عکس صفحه")
    class Meta:
        verbose_name = "داینامیک عکس صفحه اصلی"
        verbose_name_plural = "داینامیک عکس های صفحه اصلی"

class Advantage(models.Model):

    title = models.CharField(max_length=250, verbose_name="عنوان مزیت رقابتی")


    class Meta:
        verbose_name = "مزیت رقابتی"
        verbose_name_plural = "مزیت رقابتی ها"

class Footer(models.Model):
    logo = models.ImageField(upload_to='images/', verbose_name="لوگو پایین صفحه")
    title_logo = models.CharField(max_length=250, verbose_name="عنوان لوگو پایین صفحه")
    Contact_title = models.CharField(max_length=250, verbose_name="عنوان  فیلد  پایین صفحه")
    Contact_email = models.CharField(max_length=250, verbose_name="ایمیل ما")
    Contact_phone = models.CharField(max_length=11, verbose_name="شماره تلفن ما")
    Contact_address = models.CharField(max_length=250, verbose_name="آدرس ما")


    class Meta:
        verbose_name = "داینامیک پایین صفحه"
        verbose_name_plural = "داینامیک پایین صفحه ها"
