# Generated by Django 5.0.2 on 2024-02-29 09:44

import datetime
import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_remove_product_viewset_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_time',
            field=django_jalali.db.models.jDateField(blank=True, default=datetime.date(2024, 2, 29), null=True, verbose_name='تاریخ ثبت محصول'),
        ),
    ]