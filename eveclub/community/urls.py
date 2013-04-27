from django.conf.urls import patterns, include, url

urlpatterns = patterns('community.views',
    url(r'^$', 'community'),
    url(r'^topic/new/$', 'topic_new'),
    url(r'^post/new/$', 'post_new'),
    url(r'^post/edit/(?P<post_id>\d+)/$', 'post_edit'),
    url(r'^post/get_for_reply/(?P<post_id>\d+)/$', 'get_post_for_reply'),
    url(r'^upload_img/$', 'upload_img'),
)