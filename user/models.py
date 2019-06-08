# from django.db import models
# from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
# 	nickname = models.CharField(max_length=20, null=True)


# 	class UserMeta(AbstractUser.Meta):
# 		pass



from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	nickname = models.CharField(max_length=12, null=True)

	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return '<Profile %s for %s>' % (self.nickname, self.user.username)

def get_nickname(self):
	if Profile.objects.filter(user=self).exists():
		profile = Profile.objects.get(user=self)
		return profile.nickname
	else:
		return '暂无昵称'


def get_nickname_or_username(self):
	if Profile.objects.filter(user=self).exists():
		profile = Profile.objects.get(user=self)
		return profile.nickname
	else:
		return self.username


User.get_nickname = get_nickname
User.get_nickname_or_username = get_nickname_or_username
