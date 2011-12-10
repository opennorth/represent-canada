from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

# @todo Shouldn't really be here.
def settings_processor(request):
    return {'settings': settings}

def index(request):
    context = RequestContext(request)

    try:
        address = request.REQUEST.get('address')
        context['address'] = address
    except KeyError:
        pass

    return render_to_response('index.html', context)
