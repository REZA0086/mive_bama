from django.contrib import admin
from blog.models import *


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','image', 'price')


@admin.register(Rating)
class Rating(admin.ModelAdmin):
    list_display = ('user', 'product', 'value')

@admin.register(HeaderIndex)
class HeaderIndex(admin.ModelAdmin):
    list_display = ['title']

@admin.register(TitleIndex)
class TitleIndex(admin.ModelAdmin):
    list_display = ['title']

@admin.register(SliderIndex)
class SliderIndex(admin.ModelAdmin):
    list_display = ['title','description']

@admin.register(ImageIndex)
class ImageIndex(admin.ModelAdmin):
    list_display = ['image']

@admin.register(Advantage)
class AdvantageAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ['title_logo']