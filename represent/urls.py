from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    # @see https://docs.djangoproject.com/en/1.10/releases/1.9/#passing-a-3-tuple-or-an-app-name-to-include Django 1.9
    url(r'^admin/', include(admin.site.urls)),
    url('', include('boundaries.urls')),
    url('', include('representatives.urls')),
    url('', include('postcodes.urls')),
    url('', include('finder.urls')),
]
