from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Comment(models.Model):
	comment_content = models.TextField()
	cteated_time = models.DateTimeField(auto_now_add=True)  # auto_now_add 用于指定创建时间
	user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)

	# content_type 三件套
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	
	root = models.ForeignKey('self', null=True, related_name="root_comment", on_delete=models.CASCADE)
	parent = models.ForeignKey('self', null=True, related_name="parent_comment", on_delete=models.CASCADE)
	reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE)


	def get_url(self):
		return self.content_object.get_url()

	def __str__(self):
		return '<Comment %s>' % self.comment_content