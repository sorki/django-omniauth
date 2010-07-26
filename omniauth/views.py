import re
from django.conf import settings
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def omnilogin(request, forms_to_render={},
        redirect_field_name=REDIRECT_FIELD_NAME,
        template_name='omniauth/login.html'):

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if not redirect_to or ' ' in redirect_to:
        redirect_to = settings.LOGIN_REDIRECT_URL

    elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
        redirect_to = settings.LOGIN_REDIRECT_URL

    if request.user.is_authenticated():
        HttpResponseRedirect(redirect_to)

    for (var_name, form) in forms_to_render.iteritems():
        if not callable(form):
            form = type(form)

        forms_to_render[var_name]=form(initial={redirect_field_name: redirect_to})

    return render_to_response(template_name,
            {'forms': forms_to_render,
             'form_list': forms_to_render.values(),
            }, context_instance=RequestContext(request))

