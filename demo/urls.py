from django.conf.urls.defaults import patterns, url 
from demo import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="location"),
)
