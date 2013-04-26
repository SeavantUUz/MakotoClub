from django.shortcuts import render_to_response
from eveclub.lib import RequestContext

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))

def page404(request):
    return render_to_response('404.html', context_instance=RequestContext(request))

def page500(request):
    return render_to_response('500.html', context_instance=RequestContext(request))
