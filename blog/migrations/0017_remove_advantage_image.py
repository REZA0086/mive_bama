# Generated by Django 5.0.2 on 2024-03-02 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_advantage_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advantage',
            name='image',
        ),
    ]
