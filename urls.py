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
    url(r'download-offline/$','reg.views.download_slno_only',name='download_offline'),
    url(r'page2/(?P<pk>\d+)/$','reg.views.page2',name='pdf_page2'),
    url(r'registered-pdf/(?P<team_hash>\d+)/$','reg.views.download_pdf_hash',name='download_pdf_hash'),
    url(r'teams/$','reg.views.teams_redirect',name='teams_redirect'),
    url(r'downloads/$','reg.views.downloads_redirect',name='downloadss_redirect')
)

from django.conf import settings
import os

if settings.SERVE_MEDIA:
    urlpatterns += patterns('', 
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': os.path.join(settings.PROJECT_ROOT,'media/')})
    )
