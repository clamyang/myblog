from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExtension, ReadDetail
from comment.models import Comment
from django.urls import reverse


class BlogType(models.Model):
	type_name = models.CharField(max_length=15)

	def __str__(self):
		return self.type_name


class Blog(models.Model, ReadNumExtension):
	title = models.CharField(max_length=30)
	blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)  # 与博客类型添加外键关联

	read_details = GenericRelation(ReadDetail)  # 通过contexttypes将 Blog 和 ReadDetail 直接关联起来。
	comments = GenericRelation(Comment)
	content = RichTextUploadingField()  # 富文本带上传图片功能的字段
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	created_time = models.DateTimeField(auto_now_add=True)  # auto_now_add 一般用于指定创建时间
	last_updated_time = models.DateTimeField(auto_now=True)  # auto_now 用于指定修改后自动保存的时间


	def get_url(self):
		return reverse('blog:blog_detail', kwargs={'blog_pk': self.pk})


	def get_email(self):
		return self.author.email

	def get_user(self):
		return self.author


	def __str__(self):
		return "<Blog %s>" % self.title


	class Meta():
		ordering = ['-created_time']  # 按照发布时间逆序排列
