#coding: utf-8

import os
from PIL import Image
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from eveclub.settings import MEDIA_ROOT
from eveclub.lib import RequestContext
from community.config import *
from community.lib import *
from community.models import *

def community(request):
    displayed_categories = []
    categories = Category.objects.filter(is_active=True)
    for category in categories:
        displayed_category = {'name': category.name}
        displayed_category['channels'] = Channel.objects.filter(is_active=True, category=category)
        displayed_categories.append(displayed_category)
    return render_to_response('community.html', {'categories': displayed_categories}, context_instance=RequestContext(request))

@error_handler
def channel_display(request, channel_id):
    try:
        chnl = Channel.objects.get(id=channel_id)
    except Channel.DoesNotExist:
        raise CommunityError(u'您访问的频道不存在！')
    if not chnl.is_active:
        raise CommunityError(u'您访问的频道已关闭！')

    sticky_topics = chnl.topics.filter(is_active=True, is_sticky=True).order_by('sticky_order')
    normal_topics = chnl.topics.filter(is_active=True, is_sticky=False)
    topics = [t for t in sticky_topics] + [t for t in normal_topics]
    return render_to_response('channel_display.html', {'channel': chnl, 'topics': topics, 'extra_js': ('community/editor.js',)}, context_instance=RequestContext(request))

@error_handler
def topic_display(request, topic_id):
    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        raise CommunityError(u'您访问的主题不存在！')
    if not topic.is_active:
        raise CommunityError(u'您访问的主题已删除！')
    chnl = topic.channel
    if not chnl.is_active:
        raise CommunityError(u'您访问的频道已关闭！')

    if topic.topic_type == 'normal':
        posts = topic.post_set.filter(is_active=True)
    topic.clicks +=1
    topic.save(update_fields=['clicks'])
    return render_to_response('topic_display.html', {'channel': chnl, 'topic': topic, 'posts': posts, 'extra_js': ('community/editor.js','community/resize_images.js',)}, context_instance=RequestContext(request))

@login_required
@error_handler
def topic_new(request):
    if request.method == 'POST':
        try:
            channel_id = int(request.POST['channel_id'])
            topic_type = request.POST['topic_type']
            title = request.POST['title'].strip()
            content = request.POST['content']
        except:
            raise CommunityError(u'您提交的信息不完整！')
        if topic_type not in ('normal', 'poll',):
            raise CommunityError(u'您发布的主题类型不正确！')
        if len(title)<2:
            raise CommunityError(u'您发布的主题标题不能少于2个字！')
        if len(content)<4:
            raise CommunityError(u'您发布的主题内容不能少于4个字！')
        try:
            channel = Channel.objects.get(id = channel_id)
        except Channel.DoesNotExist:
            raise CommunityError(u'您试图在不存在的频道发布主题！')
        if not channel.is_active:
            raise CommunityError(u'您试图在已删除的频道发布主题！')
        if channel.channel_type not in ('public',):
            raise CommunityError(u'您没有在当前频道发布主题的权限！')
    else:
        raise CommunityError(u'您的操作不正确！')

    shortcontent = content.strip()[:50]
    u = request.user
    create_author = u
    update_author = u
    topic = Topic.objects.create(title=title,
                                 channel=channel,
                                 topic_type = topic_type,
                                 shortcontent=shortcontent,
                                 create_author=create_author,
                                 update_author=update_author,
                                 )
    post = Post.objects.create(title=title,
                               author=create_author,
                               content=content,
                               topic=topic)
    u.experience += channel.topic_exp
    u.wealth     += channel.topic_wlt
    u.scores     += channel.topic_scr
    u.topic_num  += 1
    u.post_num   += 1
    u.save(update_fields=['topic_num', 'post_num', 'experience', 'wealth', 'scores'])
    return HttpResponseRedirect('/channel/%d/' % channel_id)

@login_required
@error_handler
def post_new(request):
    if request.method == 'POST':
        try:
            topic_id = int(request.POST['topic_id'])
            content = request.POST['content']
        except:
            raise CommunityError(u'您提交的信息不完整！')
        if len(content)<4:
            raise CommunityError(u'您发布的回复内容不能少于4个字！')
        try:
            topic = Topic.objects.get(id = topic_id)
        except Topic.DoesNotExist:
            raise CommunityError(u'您试图回复不存在的主题！')
        if not topic.is_active:
            raise CommunityError(u'您试图回复已删除的主题！')
        if topic.is_locked:
            raise CommunityError(u'您试图回复已锁定的主题！')
        channel = topic.channel
        if not channel.is_active:
            raise CommunityError(u'您试图回复已删除频道中的内容！')

        title = 'RE:'+topic.title
        floor = topic.post_set.order_by('-floor')[0].floor+1
        u = request.user
        Post.objects.create(title=title, author=u, content=content,topic=topic,floor=floor)
        topic.update_author = u
        topic.replies += 1
        topic.save()
        u.experience += channel.reply_exp
        u.wealth     += channel.reply_wlt
        u.scores     += channel.reply_scr
        u.post_num   += 1
        u.save(update_fields=['post_num', 'experience', 'wealth', 'scores'])
        return HttpResponseRedirect("/topic/%d/" % topic_id)
    else:
        raise CommunityError(u'您的操作不正确！')

@login_required
@error_handler
def post_edit(request, post_id):
    try:
        post = Post.objects.get(id=int(post_id))
    except Post.DoesNotExist:
        raise CommunityError(u'您试图回复不存在的帖子！')
    topic = post.topic
    if not topic.is_active:
        raise CommunityError(u'您试图编辑已删除主题中的内容！')
    if topic.is_locked:
        raise CommunityError(u'您试图回复已锁定的主题！')
    channel = topic.channel
    if not channel.is_active:
        raise CommunityError(u'您试图编辑已删除频道中的内容！')
    if request.method == 'POST':
        try:
            content = request.POST['content']
        except:
            raise CommunityError(u'您提交的信息不完整！')
        if len(content)<4:
            raise CommunityError(u'您发布的回复内容不能少于4个字！')
        post.content = content
        post.save()
        return HttpResponseRedirect("/topic/%d/" % topic.id)
    else:
        return render_to_response('post_edit.html', {'channel': channel, 'topic': topic, 'post': post, 'extra_js': ('community/editor.js','community/resize_images.js',)}, context_instance=RequestContext(request))

@login_required
def upload_img(request):
    if request.method == "POST":
        img = Image.open(request.FILES['upload_img'])
        if not os.path.exists(MEDIA_ROOT+'upload'):
            os.mkdir(MEDIA_ROOT+'upload')
        t = now()
        year = t.year
        path = '%supload/%d' % (MEDIA_ROOT, year)
        if not os.path.exists(path):
            os.mkdir(path)
        month = t.month
        path =  '%s/%d' % (path, month)
        if not os.path.exists(path):
            os.mkdir(path)
        day = t.day
        path =  '%s/%d' % (path, day)
        if not os.path.exists(path):
            os.mkdir(path)
        name = '%s.png' % t.strftime('%H%M%S%f')[:-3];
        path = '%s/%s' % (path, name)
        url = '/media/upload/%s/%s/%s/%s' % (t.year, t.month, t.day, name)
        img.save(path)
        return render_to_response('upload_img_ok.html', {'url': url, 'name': name}, context_instance=RequestContext(request))
    else:
        return render_to_response('upload_img.html', context_instance=RequestContext(request))

@login_required
def get_post_for_reply(request, post_id):
    try:
        try:
            post = Post.objects.get(id=int(post_id))
        except Post.DoesNotExist:
            raise CommunityError(u'您试图回复不存在的帖子！')
        topic = post.topic
        if not topic.is_active:
            raise CommunityError(u'您试图编辑已删除主题中的内容！')
        if topic.is_locked:
            raise CommunityError(u'您试图回复已锁定的主题！')
        channel = topic.channel
        if not channel.is_active:
            raise CommunityError(u'您试图编辑已删除频道中的内容！')
        content = post.content
        content_lines = ['>'+l.rstrip() for l in content.split('\n')]
        if len(content_lines)>6:
            content_lines = content_lines[:6]
            content_lines.append('>......')
        return HttpResponse('\n'.join(content_lines))
    except CommunityError as e:
        return HttpResponse('')
