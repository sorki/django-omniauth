from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

import fboauth.views as fb_views
import registration.views as reg_views
import django.contrib.auth.views as auth_views
import django_openid_auth.views as oid_views

from forms import (
        UniAuthForm, IndexUniAuthForm, 
        UniAuthRegForm, UniPwdChangeForm,
        UniPwdResetForm, UniPwdResetConfirmForm,
        UniOidForm, IndexUniOidForm,
        )

from views import omnilogin

from django.utils.functional import curry

terminal_url = getattr(settings, 'LOGIN_REDIRECT_URL')
custom_oid_failure = curry(oid_views.default_render_failure,
        template_name='omniauth/openid/failure.html')
custom_fb_failure = curry(fb_views.default_render_failure,
        template_name='omniauth/fboauth/failure.html')

urlpatterns = patterns('',
    # Generic
    url(r'^login/',
        omnilogin,
        {'forms_to_render': {
            'auth_form': IndexUniAuthForm,
            'oid_form': IndexUniOidForm
            }
        },
        name='omni_login'),

   url(r'logout/$',
       auth_views.logout,
       {'template_name': 'omniauth/auth/logout.html'},
       name='omni_logout'),

   url(r'^auth/logout_then_login/$',
       auth_views.logout_then_login,
       name='omni_logout_then_login'),

    # OpenID
    url(r'^oid/login/$',
        oid_views.login_begin,
        {'form': UniOidForm, 
         'template_name': 'omniauth/openid/login.html',
         'login_complete': 'oid_complete',
         'render_failure': custom_oid_failure},
        name='oid_login'),
    url(r'^oid/complete/$',
        oid_views.login_complete,
        {'render_failure': custom_oid_failure},
        name='oid_complete'),

    # FB
    url(r'fb/start/$',
        'fboauth.views.start',
        name='fboauth_start'),
    url(r'fb/complete/$', 
        'fboauth.views.complete', 
        {'render_failure': custom_fb_failure},
        name='fboauth_complete'),



    # Auth
    url(r'^auth/register/$',
        reg_views.register,
        {'backend': 'registration.backends.simple.SimpleBackend',
         'success_url': terminal_url,
         'form_class': UniAuthRegForm,
         'template_name': 'omniauth/auth/register.html'},
        name='auth_register'),
    url(r'^registration_closed/$',
        direct_to_template,
        {'template': 'omniauth/registration_closed.html'},
        name='registration_disallowed'),

    url(r'^auth/login/$', 
        auth_views.login, 
        {'template_name': 'omniauth/auth/login.html',
         'authentication_form': UniAuthForm}, 
        name='auth_login'),

   url(r'^auth/password/change/$',
       auth_views.password_change,
       {'template_name': 'omniauth/auth/password_change.html',
        'password_change_form': UniPwdChangeForm},
       name='auth_password_change'),

   url(r'^auth/password/change/done/$',
       auth_views.password_change_done,
       {'template_name': 'omniauth/auth/password_change_done.html'},
       name='auth_password_change_done'),

   url(r'^auth/password/reset/$',
       auth_views.password_reset,
       {'template_name': 'omniauth/auth/password_reset.html',
        'email_template_name': 'omniauth/auth/password_reset_email.html',
        'password_reset_form': UniPwdResetForm},
       name='auth_password_reset'),

   url(r'^auth/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
       auth_views.password_reset_confirm,
       {'template_name': 'omniauth/auth/password_reset_confirm.html',
        'set_password_form': UniPwdResetConfirmForm},
       name='auth_password_reset_confirm'),

   url(r'^auth/password/reset/complete/$',
       auth_views.password_reset_complete,
       {'template_name': 'omniauth/auth/password_reset_complete.html'},
       name='auth_password_reset_complete'),

   url(r'^auth/password/reset/done/$',
       auth_views.password_reset_done,
       {'template_name': 'omniauth/auth/password_reset_done.html'},
       name='auth_password_reset_done'),
)

