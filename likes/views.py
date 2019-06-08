from django.shortcuts import render
from django.db.models import F
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import LikeCount, LikeRecord


def ErrorRes(code, message):
	data = {}
	data['status'] = 'error'
	data['code'] = code
	data['message'] = message
	return JsonResponse(data)


def SuccessRes(liked_num):
	data = {}
	data['status'] = 'success'
	data['liked_num'] = liked_num
	return JsonResponse(data)


def like_change(request):
	user = request.user
	if not user.is_authenticated:
		return ErrorRes(400, '请登录后再点赞')
	# 获取数据
	content_type = request.GET.get('content_type')
	object_id = request.GET.get('object_id')
	try:
		blog_ct_obj = ContentType.objects.get(model=content_type).model_class()
		blog_obj = blog_ct_obj.objects.get(pk=object_id)
	except Exception as e:
		return ErrorRes(401, '对象不存在') 
	ct = ContentType.objects.get(model=content_type)
	if request.GET.get('is_like') == 'true':
		# 点赞
		like_record, created = LikeRecord.objects.get_or_create(content_type=ct, object_id=object_id, user=user)
		if created:
			# 未点过赞
			obj, created = LikeCount.objects.get_or_create(content_type=ct, object_id=object_id)
			obj.liked_comment = F('liked_comment') + 1
			obj.save()
			obj.refresh_from_db()
			return SuccessRes(obj.liked_comment)
		else:
			# 已点赞，不能重复点赞
			return ErrorRes(402, '不能重复点赞')
	else:
		# 有点赞记录，取消点赞
		if LikeRecord.objects.filter(content_type=ct, object_id=object_id, user=user).exists():
			# 删除点赞记录
			obj = LikeRecord.objects.get(content_type=ct, object_id=object_id, user=user)
			obj.delete()
			likeCountObj, created = LikeCount.objects.get_or_create(content_type=ct, object_id=object_id)
			if not created:
				# 点赞总数减 1
				likeCountObj.liked_comment -= 1
				likeCountObj.save()
				return SuccessRes(likeCountObj.liked_comment)
			else:
				return ErrorRes(404, '数据错误')
		else:
			# 没有点赞过，不能取消
			return ErrorRes(403, '还没点赞过无法取消')