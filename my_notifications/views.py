from django.shortcuts import redirect, render, get_object_or_404
from notifications.models import Notification
from django.urls import reverse

def my_notifications(request):
	context = {}
	return render(request, 'my_notifications/my_notifications.html', context)

def my_notification(request, my_notification_pk):
	item = get_object_or_404(Notification, pk=my_notification_pk)
	item.unread = False
	item .save()
	return redirect(item.data['url'])

def delete_read(request):
	notifications = request.user.notifications.read()
	notifications.delete()
	return redirect(reverse('my_notifications'))