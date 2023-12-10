from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles import views
from django.urls import include, path, re_path

admin.autodiscover()

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('', include('boundaries.urls')),
    path('', include('representatives.urls')),
    path('', include('postcodes.urls')),
    path('', include('finder.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r"^static/(?P<path>.*)$", views.serve),
    ]
