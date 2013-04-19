from django.conf.urls import patterns, include, url

urlpatterns = patterns('community.views',
    url(r'^$', 'community'),
)