from django.conf import settings
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

def index(request):
    context = { 'settings': settings }

    try:
        address = request.REQUEST.get('address')
        context['address'] = address
    except KeyError:
        pass

    context['default_search_text'] = 'Enter an address or drag the pin on the map'
    context['demo_js'] = render_to_string('demo.js', context)
    return render_to_response('index.html', context)
