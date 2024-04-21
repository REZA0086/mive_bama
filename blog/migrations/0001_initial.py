# Generated by Django 5.0.1 on 2024-04-20 12:52

import datetime
import django.db.models.deletion
import django_jalali.db.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advantage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='عنوان مزیت رقابتی')),
            ],
            options={
                'verbose_name': 'مزیت رقابتی',
                'verbose_name_plural': 'مزیت رقابتی ها',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='images/', verbose_name='عکس دسته بندی')),
                ('name', models.CharField(max_length=250, verbose_name='نام دسته بندی')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='Footer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to='images/', verbose_name='لوگو پایین صفحه')),
                ('title_logo', models.CharField(max_length=250, verbose_name='عنوان لوگو پایین صفحه')),
                ('Contact_title', models.CharField(max_length=250, verbose_name='عنوان  فیلد  پایین صفحه')),
                ('Contact_email', models.CharField(max_length=250, verbose_name='ایمیل ما')),
                ('Contact_phone', models.CharField(max_length=11, verbose_name='شماره تلفن ما')),
                ('Contact_address', models.CharField(max_length=250, verbose_name='آدرس ما')),
            ],
            options={
                'verbose_name': 'داینامیک پایین صفحه',
                'verbose_name_plural': 'داینامیک پایین صفحه ها',
            },
        ),
        migrations.CreateModel(
            name='HeaderIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='عنوان بالا صفحه')),
                ('logo', models.ImageField(upload_to='images/', verbose_name='لوگو بالا صفحه')),
            ],
            options={
                'verbose_name': 'داینامیک هدر صفحه اصلی',
                'verbose_name_plural': 'داینامیک هدر های صفحه',
            },
        ),
        migrations.CreateModel(
            name='ImageIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/', verbose_name='عکس صفحه')),
            ],
            options={
                'verbose_name': 'داینامیک عکس صفحه اصلی',
                'verbose_name_plural': 'داینامیک عکس های صفحه اصلی',
            },
        ),
        migrations.CreateModel(
            name='SliderIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='عنوان اسلایدر')),
                ('description', models.TextField(verbose_name='متن اسلایدر')),
                ('image', models.ImageField(upload_to='images/', verbose_name='عکس اسلایدر')),
            ],
            options={
                'verbose_name': 'داینامیک اسلایدر صفحه اصلی',
                'verbose_name_plural': 'داینامیک اسلایدر های صفحه اصلی',
            },
        ),
        migrations.CreateModel(
            name='TitleIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/', verbose_name='عکس بالا صفحه اصلی')),
                ('title', models.CharField(max_length=250, verbose_name='عنوان ')),
                ('title1', models.CharField(max_length=250, verbose_name='عنوان 1')),
                ('title2', models.CharField(max_length=250, verbose_name='عنوان 2')),
                ('title3', models.CharField(max_length=250, verbose_name='عنوان 3')),
                ('title4', models.CharField(max_length=250, verbose_name='عنوان 4')),
            ],
            options={
                'verbose_name': 'داینامیک عکس بالای صفحه اصلی',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/', verbose_name='عکس محصول')),
                ('title', models.CharField(max_length=250, verbose_name='عنوان محصول')),
                ('price', models.DecimalField(decimal_places=0, max_digits=11, verbose_name='قیمت')),
                ('discount', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='تخفیف')),
                ('created_time', django_jalali.db.models.jDateField(blank=True, default=datetime.date(2024, 4, 20), null=True, verbose_name='تاریخ ثبت محصول')),
                ('order_count', models.IntegerField(default=0, verbose_name='تعداد فروش')),
                ('visited_count', models.IntegerField(default=0, verbose_name='تعداد بازدید')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.category', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='مقدار امتیاز')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.product', verbose_name='امتیاز محصول')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر امتیاز دهنده')),
            ],
            options={
                'verbose_name': 'امتیاز محصول',
                'verbose_name_plural': 'امتیاز محصولات',
            },
        ),
    ]
