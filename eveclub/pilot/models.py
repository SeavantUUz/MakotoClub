#coding: utf-8

from django.db import models
from django.contrib.auth.models import AbstractUser, update_last_login
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone
from datetime import date
from pilot.config import *

GENDER_CHOICES = (
    (u'保密', u'保密'),
    (u'男', u'男'),
    (u'女', u'女'),
    (u'伪娘', u'伪娘'),
    (u'伪狼', u'伪狼'),
    (u'秀吉', u'秀吉'),
    (u'扶他', u'扶他'),
    (u'自由转换', u'自由转换'),
)

def update_pilot_current_login(sender, request, user, **kwargs):
    """
    用户登录后更新本次登录的时间和IP，并且增加登录相关的统计值
    """
    user.current_login    =  timezone.now()
    user.current_login_ip =  request.META.get('REMOTE_ADDR', '0.0.0.0')
    user.login_times      += 1
    user.scores           += LOGIN_SCR
    user.experience       += LOGIN_EXP
    user.wealth           += LOGIN_WLT
    user.save(update_fields=['current_login', 'current_login_ip', 'login_times', 'scores', 'experience', 'wealth'])

def update_pilot_last_login(sender, user, **kwargs):
    """
    用户注销后将本次登录的时间和IP存入上次登录的时间和IP
    """
    user.last_login = user.current_login
    user.last_login_ip = user.current_login_ip
    user.save(update_fields=['last_login', 'last_login_ip'])

user_logged_in.disconnect(update_last_login)    # 去掉django.contrib.auth的默认登录更新操作
user_logged_in.connect(update_pilot_current_login)
user_logged_out.connect(update_pilot_last_login)

class Pilot(AbstractUser):
    """
    在Django自带的用户类基础上略做扩展的克隆飞行员类，增加了上次、本次登录时间和IP的记录
    """
    current_login = models.DateTimeField(u'本次登录时间', default=timezone.now)
    current_login_ip = models.GenericIPAddressField(u'本次登录IP', default='0.0.0.0')
    last_login_ip = models.GenericIPAddressField(u'上次登录IP', default='0.0.0.0')
    login_times = models.PositiveIntegerField(u'登录次数', default=0)
    topic_num = models.PositiveIntegerField(u'发布主题数', default=0)
    post_num = models.PositiveIntegerField(u'发布帖子数', default=0)
    scores = models.PositiveIntegerField(u'积分', default=0)
    experience = models.PositiveIntegerField(u'经验', default=0)
    wealth = models.PositiveIntegerField(u'财富', default=0)
    gravatar = models.ImageField(u'头像', upload_to='face/%Y/%m', default='gravatar/default.png')
    gender = models.CharField(u'性别', choices=GENDER_CHOICES, max_length=10, default=u'保密')
    signature = models.CharField(u'签名', max_length=200, blank=True)
    birthday = models.DateField(u'生日', auto_now=False, auto_now_add=False, default=date(1980, 1, 1))
    residence = models.CharField(u'居住地', blank=True, max_length=100)
    yy = models.CharField(u'YY号', blank=True, max_length=100)
    qq = models.CharField(u'QQ号', blank=True, max_length=100)

    class Meta:
        verbose_name = u'克隆飞行员'
        verbose_name_plural = u'克隆飞行员'

class ResetRequest(models.Model):
    username = models.CharField(max_length=30, unique=True)
    code = models.CharField(max_length=16)
    expire_time = models.DateTimeField()
    def __unicode__(self):
        return self.username
    class Meta:
        verbose_name = u'重置密码请求'
        verbose_name_plural = u'重置密码请求'
