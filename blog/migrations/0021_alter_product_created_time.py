# Generated by Django 5.0.2 on 2024-03-10 13:01

import datetime
import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_alter_footer_options_alter_headerindex_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_time',
            field=django_jalali.db.models.jDateField(blank=True, default=datetime.date(2024, 3, 10), null=True, verbose_name='تاریخ ثبت محصول'),
        ),
    ]