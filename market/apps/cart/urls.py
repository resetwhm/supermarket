from django.conf.urls import url

from cart.views import shopcart, addcart, pay
from person.views import login, myregister, member, allorder, gladdress, info, forgetpassword

urlpatterns = [
    url(r'^shopcart/$', shopcart, name='shopcart'),  # 购物车
    url(r'^addcart/$', addcart, name='addcart'),  #添加购物车
    url(r'^pay/$', pay, name='pay'),  #支付成功
]
