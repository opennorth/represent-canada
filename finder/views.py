from django import http
from django.conf import settings
from django.shortcuts import render_to_response
from django.utils.translation import check_for_language
from django.utils.http import is_safe_url


def index(request):
    return render_to_response('index.html')


def api(request):
    return render_to_response('api.html')


def data(request):
    return render_to_response('data.html')


def demo(request):
    return render_to_response('demo.html')


def government(request):
    return render_to_response('government.html')


def privacy(request):
    return render_to_response('privacy.html')


# @see django/views/i18n.py
def set_language(request):
    next = request.REQUEST.get('next')
    if not is_safe_url(url=next, host=request.get_host()):
        next = request.META.get('HTTP_REFERER')
        if not is_safe_url(url=next, host=request.get_host()):
            next = '/'
    response = http.HttpResponseRedirect(next)
    lang_code = request.GET.get('language', None)
    if lang_code and check_for_language(lang_code):
        if hasattr(request, 'session'):
            request.session['django_language'] = lang_code
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response
