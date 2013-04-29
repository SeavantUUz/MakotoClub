#coding: utf-8

import functools
from django.shortcuts import render_to_response
from eveclub.lib import RequestContext

class CommunityError(Exception):
    def __init__(self, message):
        self.message = message
    def __unicode__(self):
        return self.message

def error_handler(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            result = view_func(request, *args, **kwargs)
        except CommunityError as e:
            return render_to_response('error.html', {'message': e.message}, context_instance=RequestContext(request))
        return result
    return wrapper