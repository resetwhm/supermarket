from django.conf.urls import url

from order.views import tureorder
from person.views import login, myregister, member, allorder, gladdress, info, forgetpassword

urlpatterns = [
    url(r'^ture/$', tureorder, name='ture'),  # 确认订单

]
