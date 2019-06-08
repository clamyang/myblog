from django import template
from ..models import Comment
from ..forms import CommentForm
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.simple_tag()
def get_comment_count(obj):
	content_type = ContentType.objects.get_for_model(obj)
	data = Comment.objects.filter(content_type=content_type, object_id=obj.id).count()
	return data


@register.simple_tag()
def get_comments(obj):
	content_type = ContentType.objects.get_for_model(obj)
	return Comment.objects.filter(content_type=content_type, object_id=obj.id, parent=None).order_by('-cteated_time')


@register.simple_tag()
def get_comment_form(obj):
	content_type = ContentType.objects.get_for_model(obj)
	data = {
		"content_type": content_type.model,   # 获取到对应的models字符串
		"object_id": obj.id,
		"reply_comment_id": 0  # 要被回复的那条评论的id
	}
	comment_form = CommentForm(initial=data)  # 添加初始值,即给前端页面的values属性赋值
	return comment_form