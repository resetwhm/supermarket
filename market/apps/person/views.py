import hashlib
import random
import re
import uuid

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django_redis import get_redis_connection

from order.models import Order_info
from person.forms import MyregisterFrom, MyloginForm, ForgetFrom
from person.helper import set_password, my_login, send_sms

from person.models import register, User_info, Address


def check(old):
    def inner(request, *args, **kwargs):
        id = request.session.get('id')
        if id:
            return old(request, *args, **kwargs)
        else:
            return redirect('person:login')

    return inner


def login(request):
    ''' 登录 '''
    if request.method == 'POST':
        data = request.POST
        form = MyloginForm(data)
        if form.is_valid():
            # tel = form.cleaned_data.get('tel')
            # password = form.cleaned_data.get('password')
            # h = hashlib.md5(password.encode('utf-8'))
            # password = h.hexdigest()
            # data = register.objects.filter(tel=tel, password=password).first()

            # 验证成功后将登陆标识放到session中
            user = form.cleaned_data.get('user')
            # 调用登陆的方法,放在helper模块中的
            my_login(request, user)
            # 跳转到用户中心页面
            next = request.GET.get('next')
            if next:
                return redirect(next)
            else:
                return redirect('person:member')
            # if data:
            #     request.session['id'] = data.id
            #     return redirect('person:member')
            # else:
            #     # 如果找到数据,则进入个人中心.否则,跳转到注册页面
            #     return redirect('person:register')
        else:
            context = {
                'error': form.errors
            }
            return render(request, 'person/login.html', context)

    else:
        return render(request, 'person/login.html')


def myregister(request):
    ''' 注册 '''
    if request.method == 'POST':
        data = request.POST
        form = MyregisterFrom(data)
        if form.is_valid():
            data = form.cleaned_data
            tel = data.get('tel')
            password = data.get('password')
            password = set_password(password)
            register.objects.create(tel=tel, password=password)
            return redirect('person:login')
        else:
            context = {
                'error': form.errors
            }
            return render(request, 'person/reg.html', context)

    else:
        return render(request, 'person/reg.html')


def member(request):
    ''' 用户中心 '''
    id = request.session.get('id')
    if id:
        try:
            data = register.objects.filter(pk=id).first()
            nick = User_info.objects.filter(log_id=id).first()
        except User_info.MultipleObjectsReturned:
            return redirect('person:register')
        except User_info.DoesNotExist:
            return redirect('person:register')
        context = {
            'id': id,
            'data': data,
            'nick': nick
        }
        return render(request, 'person/member.html', context)
    else:
        return render(request, 'person/member.html')


# @check
def info(request):
    ''' 个人资料 '''
    id = request.session.get('id')
    if id:
        if request.method == 'POST':
            nickname = request.POST.get('nickname')
            head_img = request.FILES['head']
            sex = request.POST.get('sex')
            birthday = request.POST.get('birthday')
            school = request.POST.get('school')
            location = request.POST.get('location')
            hometown = request.POST.get('hometown')
            tel = request.POST.get('tel')
            id = register.objects.get(id=id)
            User_info.objects.filter(log_id=id).update(head_img=head_img, nickname=nickname, sex=sex, birthday=birthday,
                                                       school=school,
                                                       location=location,
                                                       hometown=hometown, tel=tel, log_id=id)
            return redirect('person:member')
        else:
            try:
                data = User_info.objects.filter(log_id=id).first()
            except User_info.MultipleObjectsReturned:
                return redirect('person:login')
            except User_info.DoesNotExist:
                return redirect('person:login')
            context = {
                'data': data
            }
            return render(request, 'person/infor.html', context)
    else:
        return render(request, 'person/infor.html')


def forgetpassword(request):
    ''' 忘记密码 '''
    if request.method == 'POST':
        data = request.POST
        form = ForgetFrom(data)
        if form.is_valid():
            tel = form.cleaned_data.get('tel')
            password = form.cleaned_data.get('password')
            h = hashlib.md5(password.encode('utf-8'))
            password = h.hexdigest()
            register.objects.filter(tel=tel).update(password=password)
            return redirect('person:login')
        else:
            context = {
                'error': form.errors
            }
            return render(request, 'person/forgetpassword.html', context)
    else:
        return render(request, 'person/forgetpassword.html')


# 验证码
def send_phone_code(request):
    if request.method == 'POST':
        # 获取手机号码
        tel = request.POST.get('tel')
        # 验证手机号是否正确
        phone_re = re.compile('^1[3-9]\d{9}$')
        res = re.search(phone_re, tel)
        if res:
            # 生成随机验证码
            code = "".join([str(random.randint(0, 9)) for _ in range(4)])
            # print(code)
            # 保存到redis中 ,等你验证的时候使用
            r = get_redis_connection('default')
            r.set(tel, code)
            # 设置过期时间 redis
            r.expire(tel, 120)

            # 发送短信

            # __business_id = uuid.uuid1()
            # params = "{\"code\":\"%s\",\"product\":\"源码超市\"}" % (code,)
            # send_sms(__business_id, tel, "注册验证", "SMS_2245271", params)

            print(code)
            return JsonResponse({"sta": 0})
        else:
            return JsonResponse({"sta": 1, "err": "验证码错误"})

    else:
        return JsonResponse({"sta": 1, "err": "请求方式错误"})


def gladdress(request):
    id = request.session.get('id')
    if id:
        data = Address.objects.filter(log=id, isdelete=False).order_by('-isDefault')
        context = {
            'data': data
        }
        return render(request, 'person/gladdress.html', context)
    else:
        return render(request, 'person/gladdress.html')


def allorder(request):
    id = request.session.get('id')
    order_id = request.GET.get('order_id')
    # Order_info.objects.filter(order_id=order_id).update()
    if id:
        return render(request, 'person/allorder.html')
    else:
        return render(request, 'person/allorder.html')
