from copy import copy

from django import forms

from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm)
from django_openid_auth.forms import OpenIDLoginForm
from registration.forms import RegistrationForm

from uni_form.helpers import FormHelper, Submit# , Fieldset

common_helper = FormHelper()
common_helper.add_input(Submit('login', 'Login'))

common_next_field = forms.CharField(widget=forms.widgets.HiddenInput)


class UniAuthForm(AuthenticationForm):
    helper = common_helper

class IndexUniAuthForm(UniAuthForm):
    next = common_next_field
    helper = copy(common_helper)
    helper.form_action = 'auth_login'

class UniAuthRegForm(RegistrationForm):
    helper = FormHelper()
    helper.add_input(Submit('register', 'Register'))

class UniPwdChangeForm(PasswordChangeForm):
    helper = common_helper

class UniPwdResetForm(PasswordResetForm):
    helper = common_helper

class UniPwdResetConfirmForm(SetPasswordForm):
    helper = common_helper



class UniOidForm(OpenIDLoginForm):
    helper = common_helper

class IndexUniOidForm(UniOidForm):
    next = common_next_field
    helper = copy(common_helper)
    helper.form_action = 'oid_login'
