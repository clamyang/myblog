from django import template
from ..models import LikeRecord, LikeCount
from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.simple_tag()
def get_like_num(obj):
	ct = ContentType.objects.get_for_model(obj)
	object_id = obj.id

	num_obj = LikeCount.objects.filter(content_type=ct, object_id=object_id).first()
	if num_obj:
		return num_obj.liked_comment
	else:
		return 0

@register.simple_tag(takes_context=True)  # 携带母版的相关信息
def get_like_status(context, obj):
	user = context['user']
	if not user.is_authenticated:
		return ''
	ct = ContentType.objects.get_for_model(obj)
	object_id = obj.id
	is_exists = LikeRecord.objects.filter(user=user, object_id=object_id, content_type=ct).exists()
	if is_exists:
		return 'active'
	else:
		return ''

