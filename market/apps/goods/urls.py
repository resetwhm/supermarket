from django.conf.urls import url
from django.views.decorators.cache import cache_page

from goods.views import index, detail, category, city, village, village_edit

urlpatterns = [
    # 设置缓存
    url(r'^$', cache_page(3600)(index), name='index'),
    url(r'^(?P<id>\d+).html$', detail, name='detail'),
    url(r'^category/(?P<cate_id>\d+)/(?P<order_id>\d)/$', category, name='category'),
    url(r'^city/$', city, name='city'),
    url(r'^village/$', village, name='village'),
    url(r'^village_edit/(?P<id>\d+)/$', village_edit, name='village_edit'),

]
