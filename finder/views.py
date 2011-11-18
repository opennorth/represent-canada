#!/usr/bin/env python

from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    context = RequestContext(request)

    try:
        address = request.REQUEST.get('address')
        context['address'] = address
    except KeyError:
        pass

    return render_to_response('index.html', context)
