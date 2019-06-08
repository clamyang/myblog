from django.contrib import admin
from .models import Comment

# Register your models here.

class CommentAdmin(admin.ModelAdmin):
	list_display = ('id', 'comment_content', 'cteated_time', 'content_type', 'user', 'root', 'parent')  # content_object显示对应的对象

admin.site.register(Comment, CommentAdmin)