from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
	list_display = ('id', 'read_num', 'content_object')  # content_object显示对应的对象


class ReadDetailAdmin(admin.ModelAdmin):
	list_display = ('id', 'read_num', 'date', 'content_object')

admin.site.register(models.ReadDetail, ReadDetailAdmin)