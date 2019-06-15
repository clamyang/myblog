from django.db.models.signals import post_save
from django.utils.html import strip_tags
from notifications.signals import notify
from django.dispatch import receiver
from .models import LikeRecord

@receiver(post_save, sender=LikeRecord)
def send_like_notifications(sender, instance, **kwargs):
	if instance.content_type.model == 'comment':
		verb = '你的评论-<{0}>-被<{1}>点赞'.format(strip_tags(instance.content_object.comment_content), instance.user.get_nickname_or_username())
		recipient = instance.content_object.user
	elif instance.content_type.model == 'blog':
		verb = '你的博客-<{0}>-被<{1}>点赞'.format(instance.content_object.title, instance.user.get_nickname_or_username())
		recipient = instance.content_object.author
	url = instance.content_object.get_url()
	notify.send(instance.user, recipient=recipient, verb=verb, url=url)