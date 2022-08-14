# -*- codeing = uft-8 -*-*
# @Time : 2022/8/14 10:41
# @Author : 曾佳进
# @File : urls.py
# @Software : PyCharm
from django.urls import path,include
from . import views
app_name='sales'
urlpatterns = [
    path('select_sale_chance_list/',views.select_sale_chance_list,name='select_sale_chance_list'),
    path('sale_chance_index/',views.sale_chance_index,name='sale_chance_index'),
]