# Generated by Django 5.0.2 on 2024-02-29 09:44

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0004_delete_factor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_date',
            field=django_jalali.db.models.jDateField(auto_now=True, null=True, verbose_name='تاریخ پرداخت'),
        ),
    ]