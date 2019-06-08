from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


# 登录的表单
class LoginForm(forms.Form):
	username_or_email = forms.CharField(min_length=3,
							   max_length=24,
							   label='用户名',
							   widget=forms.TextInput(
								attrs = {"class": "form-control",
										 "placeholder": "请输入用户名"}
								)
								)
	password = forms.CharField(label='密码',
							   widget=forms.PasswordInput(
									attrs = {"class":"form-control",
											 "placeholder": "请输入密码"}
								)
								)

	def clean(self):
		username_or_email = self.cleaned_data.get('username_or_email')
		password = self.cleaned_data.get('password')
		user = auth.authenticate(username=username_or_email, password=password)
		if user is None:
			if User.objects.filter(email=username_or_email).exists():
				username = User.objects.get(email=username_or_email).username
				user = auth.authenticate(username=username, password=password)
				self.cleaned_data['user'] = user
				return self.cleaned_data
			raise forms.ValidationError('用户名或密码不正确')
		else:
			self.cleaned_data['user'] = user
		return self.cleaned_data


# 注册的表单
class RegForm(forms.Form):
	username = forms.CharField(
						min_length=3,
						max_length=12,
						label='用户名',
						widget=forms.TextInput(attrs={'class': 'form-control'}))
	
	password = forms.CharField(
								min_length=6,
								max_length=12,
								label='密码',
								widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	
	re_password = forms.CharField(
								min_length=6,
								max_length=12,
								label='重复密码',
								widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	
	email = forms.EmailField(
							label='邮箱',
							widget=forms.EmailInput(attrs={'class': 'form-control'}))
	
	verification_code = forms.CharField(
								required=False,
								label='验证码',
								widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'点击“发送验证码”发送到邮箱'})
		)


	def __init__(self, *args, **kwargs):
		if 'request' in kwargs:
			self.request = kwargs.pop('request')
		super(RegForm, self).__init__(*args, **kwargs)


	def clean_username(self):
		username = self.cleaned_data.get('username')
		item = User.objects.filter(username=username)
		if item:
			raise forms.ValidationError('用户名已存在')
		else:
			return username


	def clean_email(self):
		email = self.cleaned_data.get('email')
		email = User.objects.filter(email=email)
		if email:
			raise forms.ValidationError('邮箱已经被注册')
		else:
			return email


	def clean_verification_code(self):
		verification_code = self.cleaned_data.get('verification_code', '').strip()
		print(verification_code)
		code = self.request.session.get('register_code', '')
		if verification_code == '':
			raise forms.ValidationError('验证码不能为空')
		elif not (code == verification_code):
			raise forms.ValidationError('验证码不正确')

		return verification_code


	def clean(self):
		password = self.cleaned_data.get('password')
		re_password = self.cleaned_data.get('re_password')
		if password != re_password:
			raise forms.ValidationError('两次密码不一致')
		else:
			return self.cleaned_data


# 修改昵称
class ChangeNicknameForm(forms.Form):
	nickname_new = forms.CharField(
		label='新的昵称', 
		max_length=20,
		widget=forms.TextInput(
			attrs={'class':'form-control', 'placeholder':'请输入新的昵称'}
		)
	)

	def __init__(self, *args, **kwargs):
		if 'user' in kwargs:
			self.user = kwargs.pop('user')
		super(ChangeNicknameForm, self).__init__(*args, **kwargs)


	def clean(self):
		# 判断用户是否登录
		if self.user.is_authenticated:
			self.cleaned_data['user'] = self.user
		else:
			raise forms.ValidationError('需要登录')
		return self.cleaned_data


	def clean_nickname_new(self):
		nickname_new = self.cleaned_data.get('nickname_new', '').strip()
		if nickname_new == '':
			raise forms.ValidationError("新的昵称不能为空")
		return nickname_new


# 绑定邮箱
class BindEmailForm(forms.Form):
	email = forms.EmailField(
		label='邮箱',
		widget=forms.EmailInput(
			attrs={'class':'form-control', 'placeholder':'请输入正确的邮箱'}
		)
	)
	verification_code = forms.CharField(
		label='验证码',
		required=False,
		widget=forms.TextInput(
			attrs={'class':'form-control', 'placeholder':'点击“发送验证码”发送到邮箱'}
		)
	)

	def __init__(self, *args, **kwargs):
		if 'request' in kwargs:
			self.request = kwargs.pop('request')
		super(BindEmailForm, self).__init__(*args, **kwargs)

	def clean(self):
		# 判断用户是否登录
		if self.request.user.is_authenticated:
			self.cleaned_data['user'] = self.request.user
		else:
			raise forms.ValidationError('用户尚未登录')

		# 判断用户是否已绑定邮箱
		if self.request.user.email != '':
			raise forms.ValidationError('你已经绑定邮箱')

		# 判断验证码
		code = self.request.session.get('bind_email_code', '')
		verification_code = self.cleaned_data.get('verification_code', '')
		if not (code != '' and code == verification_code):
			raise forms.ValidationError('验证码不正确')

		return self.cleaned_data

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('该邮箱已经被绑定')
		return email

	def clean_verification_code(self):
		verification_code = self.cleaned_data.get('verification_code', '').strip()
		if verification_code == '':
			raise forms.ValidationError('验证码不能为空')
		return verification_code


# 已经登录的条件下修改密码 
class ChangePassword(forms.Form):
	old_password = forms.CharField(
						label='旧密码',
						widget=forms.PasswordInput(
							attrs={'class': 'form-control',
								   'placeholder': '请输入原密码'
							}
						)
		)
	new_password = forms.CharField(
						label='新密码',
						min_length= 8,
						max_length=24,
						widget=forms.TextInput(
							attrs={'class': 'form-control',
								   'placeholder': '请输入新密码'
							}
						)
		)
	re_new_password = forms.CharField(
						label='确认新密码',
						widget=forms.PasswordInput(
							attrs={'class': 'form-control',
								   'placeholder': '请输入新密码'
							}
						)
		)

	def __init__(self, *args, **kwargs):
		if 'user' in kwargs:
			self.user = kwargs.pop('user')
		super().__init__(*args, **kwargs)


	def clean_new_password(self):
		new_password = self.cleaned_data.get('new_password', '')
		if new_password == '':
			raise forms.ValidationError('新密码不能为空')
		self.cleaned_data['new_password'] = new_password
		return new_password


	def clean_old_password(self):
		old_password = self.cleaned_data.get('old_password', '')
		if old_password is '':
			raise forms.ValidationError('旧密码不能为空')
		elif not self.user.check_password(old_password):
			raise forms.ValidationError('原密码错误')



	def clean(self):
		if not self.user.is_authenticated:
			raise forms.ValidationError('请登录后再修改密码')
		else:
			old_password = self.cleaned_data.get('old_password')
			re_new_password = self.cleaned_data.get('re_new_password')
			new_password = self.cleaned_data.get('new_password')
			if new_password != re_new_password:
				raise forms.ValidationError('两次密码不一致')
		return self.cleaned_data


# 未登录（忘记密码）
class ForgetPassword(forms.Form):
	email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入注册时使用的邮箱'}))
	verification_code = forms.CharField(required=False, label='验证码', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入验证码'}))
	new_password = forms.CharField(min_length=6, max_length=12, label='新密码', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入新密码'}))
	re_new_password = forms.CharField(min_length=6, max_length=12,label='确认密码', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请确认新密码'}))
	# new_password = forms.CharField()
	
	def __init__(self, *args, **kwargs):
		if 'request' in kwargs:
			self.request = kwargs.pop('request')
		super().__init__(*args, **kwargs)

	def clean_email(self):
		email = self.cleaned_data.get('email', '')
		if email == '':
			raise forms.ValidationError("邮箱不能为空")
		elif not User.objects.filter(email=email).exists():
			raise forms.ValidationError('该邮箱还未被注册')
		return email

	def clean_verification_code(self):
		verification_code = self.cleaned_data.get('verification_code', '')
		code = self.request.session.get('forget_pwd', '')
		print(verification_code, code)
		if verification_code == '':
			raise forms.ValidationError('验证码不能为空')
		if not (code != '' and code == verification_code):
			raise forms.ValidationError('验证码不正确')
		return verification_code

	def clean(self):
		new_password = self.cleaned_data.get('new_password', '')
		re_new_password = self.cleaned_data.get('re_new_password', '')
		if not (new_password == re_new_password):
			raise forms.ValidationError('两次密码不一致')
		return self.cleaned_data