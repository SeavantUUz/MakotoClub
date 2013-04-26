#coding: utf-8

import django.template
from eveclub.settings import *

class RequestContext(django.template.RequestContext):
    stat_js = STAT_JS
