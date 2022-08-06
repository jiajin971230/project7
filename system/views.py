from django.shortcuts import render,HttpResponse
from django.views.decorators.http import require_POST,require_GET
from .models import User
from django.http import JsonResponse
from email.header import Header  # 对中文进行编码
from email.mime.text import MIMEText  # 邮件对象
from email.utils import parseaddr, formataddr  # 格式化邮箱
import smtplib  # 发送邮件
from datetime import datetime, timedelta
import uuid
from hashlib import md5
#跳转登录页面
def login(request):
    return render(request, 'system/login.html')

#跳转注册页面
def register(request):
    return render(request, 'system/register.html')

# 验证用户名是否唯一
@require_POST
def unique_username(request):
    try:
        # 接收参数
        username=request.POST.get('username')

        #查询是否有该用户
        user=User.objects.get(username=username)

        # 有用户返回页面json
        return JsonResponse({
            'code':400,
            'msg':'用户名已存在！'
        })
    except User.DoesNotExist as e:
        # 异常信息说明用户不存在
        return JsonResponse({'code':200,'msg':'恭喜你，可以注册！'})

# 验证邮箱是否唯一
@require_POST
def unique_email(request):
    try:
        # 接收参数
        email=request.POST.get('email')

        #查询是否有该用户
        user=User.objects.get(email=email)

        # 有用户返回页面json
        return JsonResponse({
            'code':400,
            'msg':'邮箱已存在！'
        })
    except User.DoesNotExist as e:
        # 异常信息说明用户不存在
        return JsonResponse({'code':200,'msg':'恭喜你，可以注册！'})

#邮件发送
        #--------------------------------------准备数据start--------------------------------------
# 1、格式化邮箱
# 函数一般位置放与调用代码之前
def format_addr(s):
    name, addr = parseaddr(s)  # 例如：尚学堂<java_mail01@163.com>
    return formataddr((Header(name, 'utf-8').encode('utf-8'), addr))
#邮件发送
@require_POST
def send_email(request):
    try:
        # 2、准备数据
        from_addr = 'z18379095787@163.com'  # 发件人
        smtp_server = 'smtp.163.com'  # 163邮箱的smtp服务器地址
        password = 'FUOIJBWWTZVJPSKZ'  # 163邮箱的授权码
        #接收邮箱
        to_addr = request.POST.get('email')  # 收件人

        #用户名
        username=request.POST.get('username')
        #密码
        upwd=request.POST.get('password')
        #使用MD5密码加密
        upwd=md5(upwd.encode(encoding='utf-8')).hexdigest()
        # uuid的随机数的激活码
        code=''.join(str(uuid.uuid4()).split('-'))
        # 十分钟后的时间戳
        td = timedelta(minutes=10)
        ts = datetime.now() + td
        ts = int(round((ts + td).timestamp() * 1000))

        # --------------------------------------准备数据end---------------------------------------
        # --------------------------------------插入数据库数据start--------------------------------
        user=User(username=username,password=upwd,email=to_addr,code=code,timestamp=ts)
        user.save()
        # --------------------------------------插入数据库数据end--------------------------------

        # ----------------------------------------构建邮件内容对象start--------------------------
        # 构建一个发送内容对象
        html = '''
            <html>
                <body>
                    <div>
                    欢迎您注册上海尚学堂CRM系统，请点击链接激活账号：
                    <a href="">http://127.0.0.1:8000/system/active_accounts/?username={}&amp;code={}&amp;timestamp={}</a>
                </div>
                </body>
            </html>
        '''.format(username, code, ts)

        msg = MIMEText(html, 'html', 'utf-8')
        # 标准邮件需要三个头部信息：from、to和subject
        msg['From'] = format_addr(u'曾小佳<%s>' % from_addr)  # 发件人
        to_name = username  #收件人名称
        msg['To'] = format_addr(u'{}<%s>'.format(to_name) % to_addr)  # 收件人
        msg['Subject'] = Header(u'CRM系统官方系统激活邮件', 'utf-8').encode('utf-8')  # 标题
        # ----------------------------------------构建邮件内容对象end--------------------------------

        # -----------------------------------------发送邮件start------------------------------------
        server = smtplib.SMTP(smtp_server, 25)  # '25':163smtp服务器默认端口是25
        server.set_debuglevel(1)  # '1':是否显示发送日志，1（显示），0（不显示）
        server.login(from_addr, password)  # 登录邮箱
        server.sendmail(from_addr, [to_addr], msg.as_string())  # 发送邮件
        server.quit()  # 关闭发送
        # -----------------------------------------发送邮件end--------------------------------------
        # 返回页面提示信息
        return JsonResponse({'code':200,'msg':'注册成功，请请前往邮箱激活账号！&nbsp;&nbsp;<a href="https://mail.163.com/">跳转链接</a>'})
    except smtplib.SMTPException as e:
        # 返回页面提示信息
        return JsonResponse(
            {'code': 400, 'msg': '注册失败'})

# ----------------------------------------------激活账户--------------------------------------------------
@require_GET
def active_accounts(request):
   try:
        # 用户名
        username=request.GET.get('username')
        # 激活码
        code=request.GET.get('code')
        # 过期时间
        ts=request.GET.get('timestamp')

        #根据用户名环和激活码查询是否有该账号
        user= User.objects.get(username=username,code=code,timestamp=ts)

        # 根据过期时间判断账号是否有效
        now_ts=int(round(datetime.now().timestamp()* 1000))
        if now_ts>int(ts):
            #链接失效，返回提示信息 并删除数据库信息
            user.delete()
            return HttpResponse('<h1>该链接已失效，请重新注册！&nbsp;&nbsp;<a href="http://127.0.0.1:8000/register/">上海尚学堂CEM系统</h1>')
        #没过期，激活账号 清除激活码 改变状态
        user.code=''    #清除激活码
        user.status=1   #有账号
        user.save()
        #返回提示信息
        return HttpResponse('<h1>注册成功！请前往系统登录&nbsp;&nbsp;<a href="http://127.0.0.1:8000/login/">上海尚学堂CEM系统</a></h1>')
   except Exception as e:
       if isinstance(e,User.DoesNotExist):
           return HttpResponse('<h1>该链接已失效，请重新注册！&nbsp;&nbsp;<a href="http://127.0.0.1:8000/register/">上海尚学堂CEM系统</h1>')
       return HttpResponse('<h1>不好意思，网络异常，激活失败，请重新尝试！</h1>')

# -----------------------------------------------------登录账户------------------------------------------------------
@require_POST
def login_user(request):
    try:
        username=request.POST.get('username')
        password=request.POST.get('password')

        # 查询数据库用户名密码是否存在

    except User.DoesNotExist as e:
        pass
