from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include('boundaries.urls')),
    url('', include('representatives.urls')),
    url('', include('postcodes.urls')),
    url('', include('finder.urls')),
]
