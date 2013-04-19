from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

urlpatterns = patterns('pilot.views',
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout, {'template_name': 'logout.html'}),
    url(r'^signup/$', 'signup'),
    url(r'^profile/$', 'profile'),
    url(r'^updatepassword/$', 'updatepassword'),
    url(r'^updateprofile/$', 'updateprofile'),
    url(r'^updategravatar/$', 'updategravatar'),
    url(r'^forgot/$', 'forgot'),
    url(r'^reset/(?P<code>\w{16})/$', 'reset'),
    url(r'^(?P<uid>\d+)/$', 'showprofile'),
)