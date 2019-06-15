import threading
from django.db.models.signals import post_save
from notifications.signals import notify
from django.dispatch import receiver
from django.utils.html import strip_tags
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from . models import Comment

@receiver(post_save, sender=Comment)
def send_notification(sender, instance, **kwargs):
	# 站内消息通知
	if instance.reply_to == None:
		recipient = instance.content_object.get_user()
		if instance.content_type.model == 'blog':
			blog = instance.content_object
			verb = '{0} 评论了你的:《{1}》'.format(instance.user.get_nickname_or_username(), blog.title)
			url = blog.get_url() + "#comment_" + str(instance.pk)
		else:
			raise Exception('未知类型')
	else:
		recipient = instance.reply_to
		verb = '{0} 回复了你的评论:({1})'.format(instance.user.get_nickname_or_username(), strip_tags(instance.parent.comment_content))
		url = instance.content_object.get_url() + "#comment_" + str(instance.pk)

	notify.send(instance.user, recipient=recipient, verb=verb, url=url)


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


@receiver(post_save, sender=Comment)
def send_mail_notification(sender, instance, **kwargs):
	if instance.parent is not None:
		subject = '你的评论有新的回复',
		email = instance.reply_to.email
	else:
		subject = '你的博客有新评论',
		email = instance.content_object.author.email
	if email != '':
		# text = self.comment_content + self.content_object.get_url()
		context = {}
		context['comment_text'] = instance.comment_content
		context['url'] = instance.content_object.get_url()
		text = render(None, 'comment/send_mail.html', context).content.decode('utf-8')
		send_mail = SendMail(subject, text, email)
		send_mail.start()
