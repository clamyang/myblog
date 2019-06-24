import datetime
import string
import random
import time
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import auth
from django.db.models import Sum
from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import Profile
from .forms import LoginForm, RegForm, ChangeNicknameForm, BindEmailForm, ChangePassword, ForgetPassword


def login(request):
	login_form = LoginForm()
	context = {}
	if request.method == 'GET':
		login_from = LoginForm()
	else:
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user = login_form.cleaned_data['user']
			auth.login(request, user)
			return redirect(request.GET.get('from', reverse('home')))
	context['objs'] = login_form
	return render(request, 'user/login.html', context)


def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def register(request):
	context = {}
	if request.method == "GET":
		reg_form = RegForm()
	else:
		reg_form = RegForm(request.POST, request=request)
		if reg_form.is_valid():
			username = reg_form.cleaned_data['username']
			password = reg_form.cleaned_data.get('password')
			email = reg_form.cleaned_data.get('email')
			conditions = {
				'username': username,
				'password': password,
				'email': email,
			}
			user = User.objects.create_user(**conditions)
			user.save()
			del request.session['register_code']
			auth.login(request, user)
			return redirect(request.GET.get('from', '/'))
	context['objs'] = reg_form
	return render(request, 'user/register.html', context)


def logout(request):
	auth.logout(request)
	return redirect(request.GET.get('from', reverse('home')))


def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)


def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()

    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)


def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            request.user.email = email
            request.user.save()
            del request.session['bind_email_code']
            return redirect(redirect_to)
    else:
        form = BindEmailForm()

    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/bind_email.html', context)


def send_verification_code(request):
	email = request.GET.get('email', '')
	send_for = request.GET.get('send_for', '')
	data = {}
	if email != '':
		# 生成验证码
		code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
		print(code)
		now = int(time.time())
		send_code_time = request.session.get('send_code_time', 0)
		if now - send_code_time < 30:
			data['status'] = 'failed'
		else:
			request.session[send_for] = code
			print(request.session[send_for])
			request.session['send_code_time'] = now
			# 发送邮件
			send_mail(
				'绑定邮箱',
				'验证码： %s' % code,
				'1054305497@qq.com',
				[email,],
				fail_silently = False,  # 如果是False，则发送失败时候，会抛出smtplib.SMTPException异常，
				)
			data['status'] = 'success'
	else:
		data['status'] = 'failed'
	return JsonResponse(data)


def change_pwd(request):
	context = {}
	return_back_url = request.GET.get('from', reverse('home'))
	if request.method == 'GET':
		form = ChangePassword()
	else:
		form = ChangePassword(request.POST, user=request.user)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			request.user.set_password(new_password)
			request.user.save()
			auth.logout(request)
			data = {}
			data['status'] = 'success'
			return JsonResponse(data)
	context['form'] = form
	context['form_title'] = '修改密码'
	context['page_title'] = '修改密码'
	context['submit_text'] = '修改'
	context['return_back_url'] = return_back_url
	return render(request, 'user/change_pwd.html', context)

def forget_pwd(request):
	context = {}
	data = {}
	return_back_url = reverse('login')
	if request.method == 'GET':
		form = ForgetPassword()
	else:
		form = ForgetPassword(request.POST, request=request)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			new_password = form.cleaned_data.get('new_password')
			obj = User.objects.get(email=email)
			obj.set_password(new_password)
			obj.save()
			del request.session['forget_pwd']
			return redirect(reverse('login'))

	context['form'] = form
	context['form_title'] = '找回密码'
	context['page_title'] = '找回密码'
	context['submit_text'] = '提交'
	context['return_back_url'] = return_back_url

	return render(request, 'user/forget_pwd.html', context)