from django.contrib import admin
from django.urls import path
from . import views

#设置命名空间
app_name='system'

urlpatterns = [
        path('login/', views.login,name="login"),
        path('index/',views.crm_index,name='index'),
        path('register/',views.register,name='register'),
        path('system/unique_username/',views.unique_username,name='unique_username'),
        path('system/unique_email/',views.unique_email,name='unique_email'),
        path('system/send_email/',views.send_email,name='send_email'),
        path('system/active_accounts/',views.active_accounts,name='active_accounts'),
        path('system/login_user/',views.login_user,name="login_user"),
        path('system/update_password/',views.update_password,name='update_password'),
        path('logout/',views.logout,name='logout')

]
