from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

# @todo Shouldn't really be here.
def settings_processor(request):
    return {'settings': settings}

def index(request):
    return render_to_response('index.html', RequestContext(request))

def api(request):
    return render_to_response('api.html', RequestContext(request))
