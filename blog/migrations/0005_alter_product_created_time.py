# Generated by Django 5.0.2 on 2024-02-24 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_time',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='تاریخ ثبت محصول'),
        ),
    ]