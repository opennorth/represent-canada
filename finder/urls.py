from django.conf.urls import patterns, url
from finder import views

urlpatterns = patterns('',
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': ('finder')}),
    url(r'^setlang/$', views.set_language, name='set_language'),
    url(r'^api/$', views.api, name='apidoc'),
    url(r'^data/$', views.data, name='data'),
    url(r'^demo/$', views.demo, name='demo'),
    url(r'^government/$', views.government, name='government'),
    url(r'^privacy/$', views.privacy, name='privacy'),
    url(r'^$', views.index),
)
