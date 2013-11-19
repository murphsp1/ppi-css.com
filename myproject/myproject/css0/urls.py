# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('myproject.css0.views',
    #url(r'^list/$', 'list', name='list'),
    #url(r'^hello_world/$', 'hello_world'),
    url(r'^index/$','index'),
    url(r'^/$', 'index'),
	url(r'^upload/$','upload', name='upload'),
	url(r'^contact/$','contact'),
	url(r'^search/$','search'),
	url(r'^get_table_data/$','get_table_data'),
#	url(r'^init_table_data_load/$','init_table_data_load'),
)
