# Generated by Django 5.0.2 on 2024-02-24 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response_comment',
            name='response',
            field=models.CharField(max_length=300, verbose_name='متن پاسخ کامنت'),
        ),
    ]