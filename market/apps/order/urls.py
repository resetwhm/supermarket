from django.conf.urls import url

from order.views import tureorder, address, add
from person.views import login, myregister, member, allorder, gladdress, info, forgetpassword

urlpatterns = [
    url(r'^tureorder/$', tureorder, name='tureorder'),  # 确认订单
    url(r'^address/$', address, name='address'),  # 地址
    url(r'^add/$', add, name='add'),  # 添加地址
]
