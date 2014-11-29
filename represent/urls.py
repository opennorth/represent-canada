from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    (r'', include('boundaries.urls')),
    (r'', include('representatives.urls')),
    (r'', include('postcodes.urls')),
    (r'', include('finder.urls')),
)
