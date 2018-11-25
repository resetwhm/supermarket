from django.conf.urls import url

from cart.views import shopcart
from person.views import login, myregister, member, allorder, gladdress, info, forgetpassword

urlpatterns = [
    url(r'^shopcart/$', shopcart, name='shopcart'),  # 购物车

]
