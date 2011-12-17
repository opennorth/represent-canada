from django.conf.urls.defaults import include, patterns, url

from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^example/', include('example.example.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    (r'', include('boundaryservice.urls')),
    (r'', include('finder.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
