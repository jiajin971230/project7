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
from hashlib import md5
import base64

context = base64.b64encode('zengjiajin'.encode(encoding='utf-8')).decode(encoding='utf-8')
print(context)