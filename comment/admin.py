from django.contrib import admin
from comment.models import *
# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'description')

@admin.register(Response_Comment)
class ResponseCommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'response')