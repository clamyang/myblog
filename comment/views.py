from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .forms import CommentForm
from comment.models import Comment


def update_comment(request):
	referer = request.META.get('HTTP_REFERER', '/')  # 从哪个页面过来的，前一个页面的链接
	comment_form = CommentForm(request.POST, user=request.user)  # 额外给Form类传值
	if comment_form.is_valid():
		object_id = comment_form.cleaned_data.get('object_id')
		comment_text = comment_form.cleaned_data.get('comment_text')
		content_type = comment_form.cleaned_data.get('content_type')
		content_object = comment_form.cleaned_data.get('content_object')
		user = comment_form.cleaned_data.get('user')

		parent = comment_form.cleaned_data.get('parent')
		if not parent is None:
			root = parent.root if not parent.root is None else parent
			reply_to = parent.user  #  reply_to记录的是父对象
		else:
			root = None
			reply_to = None

		conditions = {
			"object_id": object_id,
			"comment_content": comment_text,
			"content_object": content_object,
			"parent": parent,
			"user": user,
			"root": root,
			"reply_to": reply_to,
		}
		data = {}
		obj = Comment.objects.create(**conditions)
		if parent is not None:
			data['reply_to'] = obj.reply_to.get_nickname_or_username()
		else:
			data['reply_to'] = ''

		# 发送邮件
		obj.send_mail()
		data['status'] = 'success'
		data['pk'] = obj.id
		data['username'] = obj.user.get_nickname_or_username()
		data['created_time'] = obj.cteated_time.strftime("%Y-%m-%d %H:%M:%S")  # 格式化datime对象
		data['comment_content'] = obj.comment_content
		data['root_pk'] = obj.root_id if not obj.root is None else None
		data['content_type'] = ContentType.objects.get_for_model(obj).model
	else:
		data = {}
		data['status'] = 'failed'
		data['message'] = list(comment_form.errors.values())[0][0]
	return JsonResponse(data)
