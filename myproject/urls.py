# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^css0/', include('myproject.css0.urls')),
	(r'^$', RedirectView.as_view(url='/css0/index/')), # Just for ease of use.
	(r'^admin/', include(admin.site.urls)),
	url(r'^404/$', TemplateView.as_view(template_name="404.html"), name="404"),
    url(r'^500/$', TemplateView.as_view(template_name="500.html"), name="500"),
) 

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
