from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.mail import send_mail
import threading
from django.shortcuts import render

class SendMail(threading.Thread):
	def __init__(self, subject, text, email, fail_silently=False):
		self.subject = subject
		self.text = text
		self.email = email
		self.fail_silently = fail_silently
		threading.Thread.__init__(self)

	def run(self):
		send_mail(self.subject,
				  self.text, 
				  settings.EMAIL_HOST_USER, 
				  [self.email,], 
				  self.fail_silently)



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

	def send_mail(self):
		if self.parent is not None:
			subject = '你的评论有新的回复',
			email = self.reply_to.email
		else:
			subject = '你的博客有新评论',
			email = self.content_object.author.email
		if email != '':
			# text = self.comment_content + self.content_object.get_url()
			context = {}
			context['comment_text'] = self.comment_content
			context['url'] = self.content_object.get_url()
			text = render(None, 'comment/send_mail.html', context).content.decode('utf-8')
			send_mail = SendMail(subject, text, email)
			send_mail.start()



	def __str__(self):
		return '<Comment %s>' % self.comment_content