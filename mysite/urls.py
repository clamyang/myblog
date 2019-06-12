"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'home_page'

urlpatterns = [
	# 首页
	path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    # ckeditor（富文本编辑器）的默认配置信息
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('comment/', include('comment.urls')),  # 评论路由
    path('likes/', include('likes.urls')),  # 点赞路由
    path('user/', include('user.urls')),
    path('notifications/', include('notifications.urls'), name='notifications'),
    path('my_notifications/', views.my_notifications, name='my_notifications')
]

# 配置MEDIA的存储路径。
urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)