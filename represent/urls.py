from django.urls import include, path, re_path
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('', include('boundaries.urls')),
    path('', include('representatives.urls')),
    path('', include('postcodes.urls')),
    path('', include('finder.urls')),
]
