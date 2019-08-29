from django.urls import path
from django.contrib.auth.views import LoginView
from .views import logout_view, register


urlpatterns = [
    # 登录
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    # 注销
    path('logout/', logout_view, name='logout'),
    # 注册
    path('register/', register, name='register'),
]