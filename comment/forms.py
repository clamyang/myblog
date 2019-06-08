from django import forms
from ckeditor.widgets import CKEditorWidget
from django.db.models import ObjectDoesNotExist
from . models import Comment
from django.contrib.contenttypes.models import ContentType

class CommentForm(forms.Form):
	content_type = forms.CharField(widget=forms.HiddenInput)  # 隐藏该input标签
	object_id = forms.CharField(widget=forms.HiddenInput)
	# label=False，不使用label标签
	comment_text = forms.CharField(error_messages={"required": "评论不能为空"}, label=False, widget=CKEditorWidget(config_name="comment_ckeditor"))
	reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))

	def __init__(self, *args, **kwargs):
		if 'user' in kwargs:
			self.user = kwargs.pop('user')
		super(CommentForm, self).__init__(*args, **kwargs)  # 调用父类的__init__()方法


	def clean(self):
		# 登录验证
		if self.user.is_authenticated:
			self.cleaned_data['user'] = self.user  # 将用户信息添加到cleaned_data中
		else:
			raise forms.ValidationError("请登录")

		# 评论对象验证
		content_type = self.cleaned_data.get('content_type')
		object_id = self.cleaned_data.get('object_id')
		try:
			model_class = ContentType.objects.get(model=content_type).model_class()
			obj = model_class.objects.get(pk=object_id)
			self.cleaned_data['content_object'] = obj
		except ObjectDoesNotExist:
			raise forms.ValidationError("评论对象不存在")
		return self.cleaned_data


	# 根据reply_comment_id检查是否存在父级评论
	def clean_reply_comment_id(self):
		reply_comment_id = self.cleaned_data['reply_comment_id']
		if reply_comment_id == 0:
			self.cleaned_data['parent'] = None
		elif Comment.objects.filter(pk=reply_comment_id).exists():
			parent = Comment.objects.get(pk=reply_comment_id)
			self.cleaned_data['parent'] = parent
		else:
			raise forms.ValidationError("评论对象不存在")
		return reply_comment_id