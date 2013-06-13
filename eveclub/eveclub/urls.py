from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from eveclub.settings import DEBUG, MEDIA_ROOT, STATIC_ROOT

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'specialpages.views.about'),
    url(r'^about/$', 'specialpages.views.about'),
    url(r'^404/$', 'specialpages.views.page404'),
    url(r'^500/$', 'specialpages.views.page500'),
    url(r'^pilot/', include('pilot.urls')),
    url(r'^community/', include('community.urls')),
    url(r'^channel/(?P<channel_id>\d+)/$', 'community.views.channel_display'),
    url(r'^channel/(?P<channel_id>\d+)/p(?P<page>\d+)/$', 'community.views.channel_display'),
    url(r'^topic/(?P<topic_id>\d+)/$', 'community.views.topic_display'),
    url(r'^topic/(?P<topic_id>\d+)/p(?P<page>\d+)/$', 'community.views.topic_display'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
)

if DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': STATIC_ROOT}),
    )
else:
    handler404 = 'specialpages.views.page404'
    handler500 = 'specialpages.views.page500'
