from django.conf.urls import url

from order.views import tureorder, address, add, edit, addedit, delete, default, order,addorder
from person.views import login, myregister, member, allorder, gladdress, info, forgetpassword

urlpatterns = [
    url(r'^tureorder/$', tureorder, name='tureorder'),  # 确认订单
    url(r'^order/$', order, name='order'),  # 确认订单
    url(r'^address/$', address, name='address'),  # 地址
    url(r'^addedit/$', addedit, name='addedit'),  # 地址
    url(r'^add/$', add, name='add'),  # 添加地址
    url(r'^edit/(?P<id>\d+)/$', edit, name='edit'),  # 修改地址
    url(r'^delete/$', delete, name='delete'),  # 删除地址
    url(r'^default/$', default, name='default'),  # 设置为默认值地址
    url(r'^addorder/$', addorder, name='addorder'),  # 设置为默认值地址
]
