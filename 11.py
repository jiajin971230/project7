# -*- codeing = uft-8 -*-*
# @Time : 2022/8/3 7:08
# @Author : 曾佳进
# @File : 11.py
# @Software : PyCharm
from email.header import Header #对中文进行编码
from email.mime.text import MIMEText    #邮件对象
from email.utils import parseaddr,formataddr    #格式化邮箱
import smtplib  #发送邮件
from datetime import datetime,timedelta
import uuid
from system.models import User


td = timedelta(minutes=10)
ts = datetime.now() + td
ts=int(round((ts + td).timestamp()*1000))
print(ts)

# today = datetime.now()  # 获取今天时间
# print("当前日期是：{}".format(today))
# end_time = int(round(today.timestamp()*1000))  # 取今天时间为查询结束时间，并转为13位时间戳（int()表示保留整数部分）
# offset = timedelta(days=-30)  # 定义偏移量，即与当前时间的时间间隔
# start_time = int(round((today + offset).timestamp()*1000))  # 定义查询开始时间=当前时间回退30天，转为时间戳