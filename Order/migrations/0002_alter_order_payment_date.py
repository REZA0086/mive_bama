# Generated by Django 5.0.2 on 2024-02-26 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_date',
            field=models.DateField(auto_now=True, null=True, verbose_name='تاریخ پرداخت'),
        ),
    ]
