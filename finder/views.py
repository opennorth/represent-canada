from django.conf import settings
from django.shortcuts import render_to_response

def index(request):
    context = { 'settings': settings }

    try:
        address = request.REQUEST.get('address')
        context['address'] = address
    except KeyError:
        pass

    return render_to_response('index.html', context)
