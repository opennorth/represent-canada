from django import http
from django.conf import settings
from django.shortcuts import render
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import check_for_language


def index(request):
    return _render('index.html', request)


def api(request):
    return _render('api.html', request)


def data(request):
    return _render('data.html', request)


def demo(request):
    return _render('demo.html', request)


def government(request):
    return _render('government.html', request)


def privacy(request):
    return _render('privacy.html', request)


def _render(template_name, request):
    return render(request, template_name)


# @see django/views/i18n.py
def set_language(request):
    next = request.GET.get('next')
    if not url_has_allowed_host_and_scheme(url=next, host=request.get_host()):
        next = request.headers.get('referer')
        if not url_has_allowed_host_and_scheme(url=next, host=request.get_host()):
            next = '/'
    response = http.HttpResponseRedirect(next)
    lang_code = request.GET.get('language')
    if lang_code and check_for_language(lang_code):
        if hasattr(request, 'session'):
            request.session['_language'] = lang_code
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response
