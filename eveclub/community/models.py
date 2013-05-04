#coding: utf-8

from django.db import models
from pilot.models import Pilot
from community.config import *

class Category(models.Model):
    name = models.CharField(u'分类名称', max_length=20)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    logo = models.ImageField(u'分类图标', upload_to='category', default='category/default.png')
    description = models.CharField(u'分类描述', max_length=200)
    display_order = models.IntegerField(u'显示顺序', default=10)
    is_active = models.BooleanField(u'可用', default=True)
    creator = models.ForeignKey(Pilot, verbose_name=u'分类创建者', related_name='created_categories')
    managers = models.ManyToManyField(Pilot, verbose_name=u'分类管理员', related_name='managed_categories')
    editors = models.ManyToManyField(Pilot, verbose_name=u'分类编辑', related_name='edited_categories', blank=True)
    class Meta:
        verbose_name = u'分类'
        verbose_name_plural = u'分类'
        ordering = ['display_order']
    def __unicode__(self):
        return self.name

class Channel(models.Model):
    name = models.CharField(u'频道名称', max_length=20)
    channel_type = models.CharField(u'频道类型', choices=CHANNEL_TYPE_CHOICES, default='public', max_length=10)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    logo = models.ImageField(u'分类图标', upload_to='category', default='category/default.png')
    description = models.CharField(max_length=200, verbose_name=u'分类描述')
    display_order = models.IntegerField(u'显示顺序', default=10)
    is_active = models.BooleanField(u'可用', default=True)
    category = models.ForeignKey(Category, verbose_name=u'所属分类', related_name='channels')
    creator = models.ForeignKey(Pilot, verbose_name=u'创建者', related_name='created_channels')
    managers = models.ManyToManyField(Pilot, verbose_name=u'频道管理员', related_name='managed_channels')
    editors = models.ManyToManyField(Pilot, verbose_name=u'频道编辑', related_name='edited_channels', blank=True)
    members = models.ManyToManyField(Pilot, verbose_name=u'成员', related_name='joined_channels', blank=True)
    blocked_users = models.ManyToManyField(Pilot, verbose_name=u'封禁用户', related_name='blocked_channels', blank=True)
    topic_exp = models.PositiveIntegerField(u'发布主题获得经验数', default=5)
    topic_scr = models.PositiveIntegerField(u'发布主题获得积分数', default=0)
    topic_wlt = models.PositiveIntegerField(u'发布主题获得财富数', default=2)
    reply_exp = models.PositiveIntegerField(u'发布回复获得经验数', default=2)
    reply_scr = models.PositiveIntegerField(u'发布回复获得积分数', default=0)
    reply_wlt = models.PositiveIntegerField(u'发布回复获得财富数', default=1)
    class Meta:
        verbose_name = u'频道'
        verbose_name_plural = u'频道'
        ordering = ['display_order']
    def __unicode__(self):
        return self.name

class Topic(models.Model):
    title = models.CharField(u'标题', max_length=100)
    channel = models.ForeignKey(Channel, verbose_name=u'所属频道', related_name='topics')
    topic_type = models.CharField(u'主题类型', choices=TOPIC_TYPE_CHOICES, default='normal', max_length=10)
    shortcontent = models.CharField(u'内容简介', max_length=500)
    create_author = models.ForeignKey(Pilot, verbose_name=u'发布作者', related_name='topics')
    create_time = models.DateTimeField(u'发布时间', auto_now_add=True)
    update_author = models.ForeignKey(Pilot, verbose_name=u'更新作者', related_name='replys')
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    clicks = models.IntegerField(verbose_name=u'点击数', default=0)
    replies = models.IntegerField(u'回复数', default=0)
    is_active = models.BooleanField(u'可用', default=True)
    is_locked = models.BooleanField(u'锁帖', default=False)
    is_sticky = models.BooleanField(u'置顶', default=False)
    sticky_order = models.IntegerField(u'置顶顺序', default=0)
    is_essence = models.BooleanField(u'精华', default=False)
    essence_level = models.PositiveIntegerField(u'精华级别', default=1)
    is_highlight = models.BooleanField(u'高亮', default=False)
    highlight_color = models.CharField(u'高亮颜色', max_length=7, default=u'#FF0000')
    is_bold = models.BooleanField(u'加粗', default=False)
    class Meta:
        verbose_name = u'主题'
        verbose_name_plural = u'主题'
        ordering = ['-update_time']
    def __unicode__(self):
        return self.title

class Post(models.Model):
    title =  models.CharField(u'标题', max_length=40)
    author = models.ForeignKey(Pilot, verbose_name=u'作者', related_name='posts')
    content =  models.TextField(u'内容', max_length=5000)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    update_author = models.ForeignKey(Pilot, verbose_name=u'作者')
    topic = models.ForeignKey(Topic, verbose_name=u'所属主题')
    floor = models.PositiveIntegerField(u'楼层', default=0)
    is_active = models.BooleanField(u'可用', default=True)
    class Meta:
        verbose_name = u'帖子'
        verbose_name_plural = u'帖子'
        ordering = ['floor']
    def __unicode__(self):
        return self.title
