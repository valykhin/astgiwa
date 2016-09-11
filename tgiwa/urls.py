# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^request_for_test/$', views.request_for_test, name='request_for_test'),
    url(r'^request_for_test/create_request/$', views.create_request, name='create_request'),
    url(r'^request_for_test/request_created/(?P<request_id>\d+)/$', views.request_created, name='request_created'),
    url(r'^test_results/(?P<request_id>\d+)/$', views.test_results, name='test_results'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^info/$', views.info, name='info'),
]