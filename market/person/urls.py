from django.conf.urls import url

from person.views import login

urlpatterns = [
    url(r'^login/$ ', login, name='login'),
]
