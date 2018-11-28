from django.conf.urls import url

from goods.views import index, detail, category, city, village

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<id>\d+).html$', detail, name='detail'),
    url(r'^category/(?P<cate_id>\d+)/(?P<order_id>\d)/$', category, name='category'),
    url(r'^city/$', city, name='city'),
    url(r'^village/$', village, name='village'),

]
