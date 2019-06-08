from django import template
from ..models import Profile

register = template.Library()

# @register.simple_tag(takes_context=True)
@register.simple_tag()
def check(user):
	# user = context['user']
	is_exists = Profile.objects.filter(user=user).exists()
	if is_exists:
		obj = Profile.objects.get(user=user)
		return obj.nickname
	else:
		return '暂无昵称，点击右侧添加'