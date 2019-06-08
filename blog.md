 - 今日内容 (5.29)
 	- 阅读计数统计的两种方法
 		- 1.通过添加外键
 			- 在另一张表中记录阅读数量
 		- 2.使用`congtengtype`方法
 			- `from django.contrib.contenttypes.models import ContentType`
 			- `from django.contrib.contenttypes.fields import GenericForeignKey`
 			- contenttype三件套
 				- `content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)`
 				- `object_id = PositiveIntegerField()` 该字段是对象的id
 				- `content_object = GenericForeignKey('content_type', 'object_id')`
 					- 通过`content_object`字段可以直接找到对应在另一张表中的对象！
 	
			- `contenttype`中对所有app下的model进行了封装（相当于一个中介把各个模型联系起来）
			- 案例1：
				```Python
					ct = ContentType.objects.get_for_model(Blog)  # 获取到contenttype的对象，get_for_model()中需要传入类、或者对象都可以
					另一种方法：
						ct = ContentType.objects.get(model='小写类名')
					from django.utils import timezone
					date = timezone.now()
					ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date)
				```
			- 将两个模型通过`contenttype`直接关联
				- `from django.contrib.contenttypes.fields import GenericRelation`
					- 导入如上这个类，添加在需要关联的模型中
						- `read_details = GenericRelation(ReadDetail)` 将blog和ReadDetail直接关联了起来。Blog的对象通过`read_details`就可以找到在`ReadDetail`中的对应关系
 	- 降低代码之间的耦合度（规范代码）


 	- annotate() 和 values() 的顺序
 		和使用 filter() 一样，作用于某个查询的 annotate() 和 values() 子句的顺序非常重要。如果 values() 子句在 annotate() 之前，就会根据 values() 子句产生的分组来计算注解。
		然而如果 annotate() 子句在 values() 之前，就会根据整个查询集生成注解。这种情况下，values() 子句只能限制输出的字段。
		- `annotate()`
			- 给前边筛选出来的所有对象添加一条信息，可以是本表中的内容，也可以是另一张表中的内容

# 缓存
 - 1.配置`settings.py`添加关于缓存的配置
 	```Python
		CACHES = {
		    'default': {
		    	# 使用数据库缓存
		        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
		        'LOCATION': 'blog_cache_table',
		    }
		}
 	```

 - 2.创建缓存表(使用数据库缓存)
 	- `python manage.py createcachetable`
 - 3.导入缓存类
 	- `from django.core.cache import cache`

# 评论功能
 - 创建评论表并通过`contenttype`与`blog`关联

 - `ContentType.objects.get(model='')` 与 `ContentType.objects.get_for_model()` 的区别
	- 一个传入字符串就行，一个需要对象
 - 通过`Form`表单进行评论(新知识点：给form表单添加初始值)
 	- 1.创建Form类
 	- 2.通过Form类生成前端页面
 	- 3.form表单的提交
 		- 1.post请求方式
 		- 2.ajax异步请求
 			- serialize()
 	- 4.在form类中进行数据验证 

 - 回复评论功能
 	- 数据库表的建立（通过自关联实现）
 	- 回复时需要的数据
 		- 回复的内容
 		- 回复的人
 		- 给哪条数据进行回复
 		- 回复的根节点


# 阅读数量统计和按日期统计阅读数量
	- 一篇博客对应一个阅读数量
	- 按日期统计，需要添加DateTimeField(auto_now_add=True)
	- 

# Form表单的使用

# 评论功能，回复评论功能

# 自定义用户模型
 - 1.继承用户模型
 	- 1.要继承`AbstractUser`并且配置在settings中配置`AUTH_USER_MODEL='model路径'`
 		- `from django.conf import settings`
 		- `from django.contrib.auth.models import AbstractUser`
 	- 2.使用`get_user_model()`获取User模型
 		- `from django.contrib.auth import get_user_model`
 		- `User = get_user_model()`
 		- 因为是将django自带的User表修改了，所以要想使用之前那张表需要用这个方法
 		- 还可以使用自定义的model类名
 		
 - 2.拓展用户模型
 	- 创建一张拓展表并且与`User`表建立一对一关系
 	- `from django.contrib.auth.models import User`
	- 在拓展表中添加额外的信息


# 邮箱使用
 - 1.将邮箱打开stamp
 - 2.在settings中配置邮箱信息
 - 3.`from django.core.mail import send_mail`
 - 4.使用send_mail方法, (title, message, from_user, to_user)