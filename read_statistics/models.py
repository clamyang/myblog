from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone


class ReadNum(models.Model):
	read_num = models.IntegerField(default=0)
	# 与ContentType模型建立关联关系
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	# 对应模型的id
	object_id = models.PositiveIntegerField()
	# 把以上两个封装成通用的外键
	content_object = GenericForeignKey('content_type', 'object_id')


class ReadNumExtension():
	def get_read_num(self):
		try:
			ct = ContentType.objects.get_for_model(self)
			read_num = ReadNum.objects.get(object_id=self.pk, content_type=ct).read_num
		except exceptions.ObjectDoesNotExist:
			return 0
		return read_num


# 当天阅读数，用以统计每日浏览量 
class ReadDetail(models.Model):
	read_num = models.IntegerField(default=0)
	date = models.DateField(default=timezone.now)  # 根据read_num和date字段来确定出当日阅读量

	# contenttype 三件套
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')  # 可以通过该字段，直接找到对应在另一个model中的对象！
