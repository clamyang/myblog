from notifications.signals import notify
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver


@receiver(post_save, sender=User)
def send_register_notification(sender, instance, **kwargs):
	if kwargs['created'] == True:
		verb = '欢迎注册，更多精彩内容等你发现'
		url = reverse('user_info')
		notify.send(instance, recipient=instance, verb=verb, url=url)