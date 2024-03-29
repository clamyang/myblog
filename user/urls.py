from django.urls import path
from . import views

urlpatterns = [
	path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('user_info/', views.user_info, name='user_info'),
    path('login_for_medal/', views.login_for_medal, name='login_for_medal'),
    path('change_nickname/', views.change_nickname, name='change_nickname'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
    path('change_pwd/', views.change_pwd, name='change_pwd'),
    path('forget_pwd/', views.forget_pwd, name='forget_pwd'),
]