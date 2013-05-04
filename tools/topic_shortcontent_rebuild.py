#!/usr/bin/python2
#coding: utf-8
import os
import sys

# 将eveclub目录加入系统路径
PROJECT_PATH = os.path.realpath(os.path.dirname(os.path.realpath(__file__))+'/../eveclub').replace('\\', '/')
platform = sys.platform
if platform.startswith('win'):
    PROJECT_PATH = PROJECT_PATH.replace('/', '\\')
sys.path.append(PROJECT_PATH)

# 设置DJANGO的settings模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eveclub.settings")

# 将所有主题的shortcontent增加到500字
from community.models import *
topic_sets = Topic.objects.all()
for t in topic_sets:
    p = t.post_set.get(floor=0)
    t.shortcontent = p.content.strip()[:500]
    t.save(update_fields=['shortcontent'])
    print t.title, 'OK'
