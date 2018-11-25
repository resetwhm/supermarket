from django.conf.urls import url

from goods.views import index, detail, category

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<id>\d+).html$', detail, name='detail'),
    url(r'^category/(?P<cate_id>\d+)/(?P<order_id>\d)/$', category, name='category'),
]
