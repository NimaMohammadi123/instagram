from atexit import register
from django.contrib import admin
from .models import Post ,PostComment

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user' , 'created' , 'image' , 'edit']
    list_filter = ['created' , 'edit']

@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['user' , 'post' , 'created']
    list_filter = ['created' , 'edit']