from django.contrib import admin
from .models import *


# Register your models here.

"""
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'passwd', 'created_at']

"""


class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'summary', 'author', 'created_time']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag,TagAdmin)
