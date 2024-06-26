from django.urls import path
from django.views.i18n import JavaScriptCatalog

from finder import views

urlpatterns = [
    path('jsi18n/', JavaScriptCatalog.as_view(packages=['finder']), name='javascript-catalog'),
    path('setlang/', views.set_language, name='set_language'),
    path('api/', views.api, name='apidoc'),
    path('data/', views.data, name='data'),
    path('demo/', views.demo, name='demo'),
    path('government/', views.government, name='government'),
    path('privacy/', views.privacy, name='privacy'),
    path('', views.index),
]
