from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^nikecup/', include('nikecup.foo.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    url(r'register/$','reg.views.register',name='register'),
    url(r'registered/(?P<pk>\d+)/$','reg.views.registered',name='registered'),
    url(r'download/(?P<pk>\d+)/$','reg.views.download',name='download_pdf'),
)

from django.conf import settings
import os

if settings.SERVE_MEDIA:
    urlpatterns += patterns('', 
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': os.path.join(settings.PROJECT_ROOT,'media/')})
    )
