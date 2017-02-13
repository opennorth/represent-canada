from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    (r'', include('boundaries.urls')),
    (r'', include('representatives.urls')),
    (r'', include('postcodes.urls')),
    (r'', include('finder.urls')),
]
