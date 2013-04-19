#coding: utf-8

from django.shortcuts import render_to_response
from django.template import RequestContext
from community.models import *

def community(request):
    displayed_categories = []
    categories = Category.objects.filter(is_active=True)
    for category in categories:
        displayed_category = {'name': category.name}
        displayed_category['channels'] = Channel.objects.filter(is_active=True, category=category)
        displayed_categories.append(displayed_category)
    return render_to_response('community.html', {'categories': displayed_categories}, context_instance=RequestContext(request))

def channel_display(request, channel_id):
    try:
        chnl = Channel.objects.get(id=channel_id)
    except Channel.DoesNotExist:
        return render_to_response('error.html', {'message': u'您访问的频道不存在！'}, context_instance=RequestContext(request))
    if not chnl.is_active:
        return render_to_response('error.html', {'message': u'您访问的频道已关闭！'}, context_instance=RequestContext(request))

    sticky_topics = chnl.topics.filter(is_active=True, is_sticky=True).order_by('sticky_order')
    normal_topics = chnl.topics.filter(is_active=True, is_sticky=False)
    topics = [t for t in sticky_topics] + [t for t in normal_topics]
    return render_to_response('channel_display.html', {'channel': chnl, 'topics': topics}, context_instance=RequestContext(request))

def topic_display(request, topic_id):
    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        return render_to_response('error.html', {'message': u'您访问的主题不存在！'}, context_instance=RequestContext(request))
    chnl = topic.channel
    if not chnl.is_active:
        return render_to_response('error.html', {'message': u'您访问的主题已删除！'}, context_instance=RequestContext(request))

    if not chnl.is_active:
        return render_to_response('error.html', {'message': u'您访问的频道已关闭！'}, context_instance=RequestContext(request))

    if topic.topic_type == 'normal':
        posts = topic.post_set.filter(is_active=True)
    topic.clicks +=1
    topic.save(update_fields=['clicks'])
    return render_to_response('topic_display.html', {'channel': chnl, 'topic': topic, 'posts': posts}, context_instance=RequestContext(request))
