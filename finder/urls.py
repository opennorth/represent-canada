from django.conf.urls import url
# @see https://docs.djangoproject.com/en/1.10/topics/i18n/translation/ Django 1.10
from django.views.i18n import javascript_catalog

from finder import views

js_info_dict = {
    'packages': ('finder',),
}

urlpatterns = [
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog'),
    url(r'^setlang/$', views.set_language, name='set_language'),
    url(r'^api/$', views.api, name='apidoc'),
    url(r'^data/$', views.data, name='data'),
    url(r'^demo/$', views.demo, name='demo'),
    url(r'^government/$', views.government, name='government'),
    url(r'^privacy/$', views.privacy, name='privacy'),
    url(r'^$', views.index),
]
