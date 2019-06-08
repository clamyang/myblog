from django.contrib import admin
from . import models

# Register your models here.

# 1.使用装饰器
# @admin.register(BlogAdmin)
class BlogAdmin(admin.ModelAdmin):
	# list_display = ('id', 'title', 'blog_type', 'read_num', 'content', 'author', 'created_time', 'last_updated_time')
	list_display = ('id', 'title', 'blog_type', 'get_read_num', 'content', 'author', 'created_time', 'last_updated_time')


# 使用django自带的后台时，
# 类要继承｀admin.ModelAdmin｀
class BlogTypeAdmin(admin.ModelAdmin):
	list_display = ('id', 'type_name')


# @admin.register(models.ReadNum)
# class ReadNumAdmin(admin.ModelAdmin):
# 	list_display = ('id', 'read_nums', 'blog')


# 2.使用如下这种方式
admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.BlogType, BlogTypeAdmin)