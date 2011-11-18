from django.conf import settings
from django.conf.urls.defaults import include, patterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.urls),

    (r'', include('boundaryservice.urls')),
    (r'', include('finder.urls')),

    # Should never be used in production, as nginx will server these paths
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        { 'document_root': settings.STATIC_ROOT,
            'show_indexes': True }),
)
