from django.conf.urls import url

from goods.views import index, detail, category

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^detail/$', detail, name='detail'),
    url(r'^category/$', category, name='category'),
]
