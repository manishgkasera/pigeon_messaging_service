from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^(?P<pk>[1-9][0-9]*)/$', MessageDetail.as_view(template_name='messages/detail.html'), name='detail'),
    url(r'^(?P<pk>[1-9][0-9]*)/delivered/$', delivered),
]