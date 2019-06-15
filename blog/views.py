from django.shortcuts import render, get_object_or_404
from . import models
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType
from comment.forms import CommentForm

# from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


#　一键导出该项目所需要的包
# pip3 freeze > requirement.txt

# 一键安装需求文档
# pip3 install -r requirement.txt


class PageCustom(object):
	def __init__(self, current_page, blogs_count,show_page=5):
		self.current_page = int(current_page)
		self.show_page = int(show_page)
		self.half = int((show_page - 1) / 2)
		self.blogs_count = int(blogs_count)
		print(self.blogs_count)


	def page(self):
		if self.current_page < self.show_page:
			begin = 1
			stop = self.show_page + 1
		else:
			if self.current_page + self.half > self.blogs_count:
				begin = self.blogs_count - self.show_page + 1
				stop = self.blogs_count  + 1
			else:
				begin = self.current_page - self.half
				stop = self.current_page + self.half + 1
		return list(range(int(begin), int(stop)))


def get_list_common_data(blogs_all_list, page_num):
	"""
	:param blogs_all_list: 所有的博客文章
	:param page_num: 当前页码
	:return context: 返回一个字典
	"""
	paginator = Paginator(blogs_all_list, 5)
	# get_page()方法自动处理类型转换或者异常
	page_of_blogs = paginator.get_page(page_num) 

	current_page_num = page_of_blogs.number # 获取当前页面
	page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

	# 加上省略标记
	if page_range[0] - 1 >= 2:
		page_range.insert(0, '...')
	if paginator.num_pages - page_range[-1] >= 2:
		page_range.append('...')

	# 首页和尾页
	if page_range[0] != 1:
		page_range.insert(0, 1)
	if page_range[-1] != paginator.num_pages:
		page_range.append(paginator.num_pages)

	blog_dates = models.Blog.objects.dates('created_time', 'month', 'DESC')  # 根据创建时间的月份的降序排列
	items = {}
	for blog_date in blog_dates:
		# 根据‘__year’和‘__month’来获取相应的博客对象
		numbers = models.Blog.objects.filter(created_time__year=blog_date.year,
										   created_time__month=blog_date.month).count()
		items[blog_date] = numbers

	context = {}
	context['page_range'] = page_range
	context['page_of_blogs'] = page_of_blogs
	context['blog_types'] = models.BlogType.objects.all()
	context['blog_dates'] = items  # 按照月份分档，每个月有多少条数据
	return context


# 获取所有的博客并展示
def blog_list(request):
	page_num = request.GET.get('page', 1)
	blogs_all_list = models.Blog.objects.all().order_by('-created_time')
	context = get_list_common_data(blogs_all_list, page_num)
	return render(request, 'blog/blog_list.html', context)


# 博客的详情页面
def blog_detail(request, blog_pk):
	# get_object_or_404() 找到该对象或者返回４０４错误
	blog = get_object_or_404(models.Blog, pk=blog_pk)
	read_cookie_key = read_statistics_once_read(request, blog)
	 
	context = {}
	context['previous_blog'] = models.Blog.objects.filter(created_time__gt=blog.created_time).last()
	context['next_blog'] = models.Blog.objects.filter(created_time__lt=blog.created_time).first()
	context['blog'] = blog
	response = render(request, 'blog/blog_detail.html', context)
	response.set_cookie(read_cookie_key, 'true')  # 设置cookie
	return response


# 根据传过来的pk，在BlogType中获取到对象。
def blog_with_type(request, blog_type_pk):
	context = {}
	page_num = request.GET.get('page', 1)
	blog = get_object_or_404(models.BlogType, pk=blog_type_pk)
	blogs_all_list = models.Blog.objects.filter(blog_type=blog).order_by('-created_time')
	context = get_list_common_data(blogs_all_list, page_num)
	return render(request, 'blog/blogs_with_type.html', context)


def blog_with_date(request, year, month):
	page_num = request.GET.get('page', 1)
	blogs_all_list = models.Blog.objects.filter(created_time__year=year, created_time__month=month)
	context = get_list_common_data(blogs_all_list, page_num)
	context['blogs_with_date'] = "%s年%s月" % (year, month)
	return render(request, 'blog/blogs_with_date.html', context)
