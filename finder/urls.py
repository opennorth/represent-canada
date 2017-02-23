from django.conf.urls import url
from django.views.i18n import JavaScriptCatalog

from finder import views

urlpatterns = [
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(packages=['finder']), name='javascript-catalog'),
    url(r'^setlang/$', views.set_language, name='set_language'),
    url(r'^api/$', views.api, name='apidoc'),
    url(r'^data/$', views.data, name='data'),
    url(r'^demo/$', views.demo, name='demo'),
    url(r'^government/$', views.government, name='government'),
    url(r'^privacy/$', views.privacy, name='privacy'),
    url(r'^$', views.index),
]
