# Generated by Django 5.0.1 on 2024-04-20 12:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='متن کامنت')),
                ('is_active', models.BooleanField(default=True, verbose_name='تایید شده/ نشده')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.product', verbose_name='کامنت محصول')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده کامنت')),
            ],
            options={
                'verbose_name': 'کامنت',
                'verbose_name_plural': 'کامنت ها',
            },
        ),
        migrations.CreateModel(
            name='Response_Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.CharField(max_length=300, verbose_name='متن پاسخ کامنت')),
                ('is_active', models.BooleanField(default=True, verbose_name='تایید شده/ نشده')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comment.comment', verbose_name='کامنت پاسخ دهی شده')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده پاسخ کامنت')),
            ],
            options={
                'verbose_name': 'جواب کامنت',
                'verbose_name_plural': 'جواب کامنت ها',
            },
        ),
    ]
