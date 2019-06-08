from django.urls import path
from . import views


app_name = 'blog'

# start with blog/
urlpatterns = [
	path('', views.blog_list, name='blog_list'),
	# http://localhost:8000/blog/1
	path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
	# path('article/<str:article_name>', views.article, name='article'),
	path('classify/<int:blog_type_pk>', views.blog_with_type, name='blog_with_type'),
	path('date/<int:year>/<int:month>', views.blog_with_date, name='blog_with_date'),

]