from django.shortcuts import render, redirect, get_object_or_404
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_past_seven_days_data, get_today_hot_read, get_yesterday_hot_read, get_past_7_data, get_past_30_hot_read
from blog.models import Blog

def home(request):
	blog_content_type = ContentType.objects.get_for_model(Blog)
	read_nums, dates = get_past_seven_days_data(blog_content_type)

	cache_data = cache.get('cache_for_today_data')  # 缓存的使用，如果缓存不存在，则加入缓存并设置过期时间
	if cache_data is None:
		data = get_today_hot_read()
		cache.set('cache_for_today_data', data, 3600)  # 设置缓存

	context = {}
	# 图表需要的数据
	context['read_nums'] = read_nums
	context['dates'] = dates
	# 过去的浏览量
	context['today_hot_data'] = get_today_hot_read()
	context['yesterday_hot_data'] = get_yesterday_hot_read(blog_content_type)
	context['past_seven_hot_read'] = get_past_7_data()
	context['past_30_hot_read'] = get_past_30_hot_read(blog_content_type)
	return render(request, 'home.html', context)


def search(request):
	search_word = request.GET.get('wd', '').strip()
	page_num = request.GET.get('page', '')

	condition = None
	for keyword in search_word:
		if condition is None:
			condition = Q(title__icontains=keyword)
		else:
			condition = condition | Q(title__icontains=keyword)
	print(condition)
	search_results = []
	if condition is not None:
		search_results = Blog.objects.filter(condition)
		result_count = search_results.count()
	else:
		result_count = 0
	paginator = Paginator(search_results, 5)
	# get_page()方法自动处理类型转换或者异常
	page_of_blogs = paginator.get_page(page_num) 

	context = {}
	context['search_word'] = search_word
	context['result_count'] = result_count
	context['page_of_blogs'] = page_of_blogs
	return render(request, 'search.html', context)

