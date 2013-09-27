# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('myproject.myapp.views',
    #url(r'^list/$', 'list', name='list'),
    url(r'^hello_world/$', 'hello_world'),
    url(r'^index/$','index'),
    url(r'^/$', 'index'),
	url(r'^upload/$','upload', name='upload'),
	url(r'^contact/$','contact'),
	url(r'^search/$','search'),
)
