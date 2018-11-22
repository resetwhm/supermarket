from django.conf.urls import url

from person.views import login, myregister, member, allorder, gladdress, info, forgetpassword, send_phone_code

urlpatterns = [
    url(r'^login/$', login, name='login'),  # 登录
    url(r'^reg/$', myregister, name='register'),  # 注册
    url(r'^member/$', member, name='member'),  # 个人中心
    url(r'^allorder/$', allorder, name='allorder'),  # 订单
    url(r'^gladdress/$', gladdress, name='gladdress'),  # 地址
    url(r'^info/$', info, name='info'),  # 个人资料
    url(r'^forget/$', forgetpassword, name='forget'),  # 忘记密码
    url(r'^send/$', send_phone_code, name='send'),  # 验证码
]
