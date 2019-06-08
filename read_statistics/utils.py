import datetime
from django.db.models import Sum
from django.utils import timezone
from blog.models import Blog
from read_statistics.models import ReadNum, ReadDetail
from django.contrib.contenttypes.models import ContentType


def read_statistics_once_read(request, obj):
	ct = ContentType.objects.get_for_model(obj)
	key = '%s_%s_has_read' % (ct.model, obj.pk)

	if not request.COOKIES.get(key):
		# 总阅读数+1
		read_num, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
		read_num.read_num += 1
		read_num.save()

		# 当天阅读数+1
		date = timezone.now().date()
		detail_obj, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
		detail_obj.read_num += 1
		detail_obj.save()

	return key


def get_past_seven_days_data(content_type):
	today = timezone.now().date()
	read_nums = []
	dates = []
	for i in range(7, 0, -1):
		date = today - datetime.timedelta(days=i-1)  # 减24小时
		dates.append(date.strftime('%m/%d'))  # date.strftime('%m/%d') 将datetime类型转换成字符串
		read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
		result = read_details.aggregate(total=Sum('read_num'))
		read_nums.append(result['total'] or 0)
	return read_nums, dates


def get_today_hot_read():
	today = timezone.now().date()
	read_details = Blog.objects.filter(read_details__date=today).values('id', 'title', 'read_details__read_num').order_by('-read_details__read_num')
	return read_details[:7]


def get_yesterday_hot_read(content_type):
	today = timezone.now().date()
	yesterday = today - datetime.timedelta(days=1)
	read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
	return read_details[:7]


# def get_past_seven_hot_read(content_type):
# 	today = timezone.now().date()
# 	date = today - datetime.timedelta(days=7)
# 	read_details = ReadDetail.objects \
# 							.filter(content_type=content_type, date__gt=date) \
# 							.values('content_type', 'object_id') \
# 							.annotate(read_num_sum=Sum('read_num')) \
# 							.order_by("-read_num_sum")
# 	return read_details[:7]


# 通过contenttype的GenericRelation直接关联
def get_past_7_data():
	today = timezone.now().date()
	date = today - datetime.timedelta(days=7)
	blogs = Blog.objects.filter(read_details__date__gte=date, read_details__date__lt=today) \
						.values('id', 'title') \
						.annotate(read_num_sum=Sum('read_details__read_num')) \
						.order_by('-read_num_sum')
	return blogs


def get_past_30_hot_read(content_type):
	today = timezone.now().date()
	date = today - datetime.timedelta(days=30)
	read_details = Blog.objects.filter(read_details__date__lt=today, 
										 read_details__date__gte=date) \
								 .values('id', 'title') \
								 .annotate(read_num_sum=Sum('read_details__read_num')) \
								 .order_by('-read_details__read_num')
	return read_details[:7]
