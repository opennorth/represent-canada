from django import http
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import check_for_language
from django.utils.http import is_safe_url


def index(request):
    return render('index.html', request)


def api(request):
    return render('api.html', request)


def data(request):
    return render('data.html', request)


def demo(request):
    return render('demo.html', request)


def government(request):
    return render('government.html', request)


def privacy(request):
    return render('privacy.html', request)


def render(template, request):
    return render_to_response(template, context_instance=RequestContext(request))


# @see django/views/i18n.py
def set_language(request):
    next = request.GET.get('next')
    if not is_safe_url(url=next, host=request.get_host()):
        next = request.META.get('HTTP_REFERER')
        if not is_safe_url(url=next, host=request.get_host()):
            next = '/'
    response = http.HttpResponseRedirect(next)
    lang_code = request.GET.get('language')
    if lang_code and check_for_language(lang_code):
        if hasattr(request, 'session'):
            request.session['_language'] = lang_code
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response
