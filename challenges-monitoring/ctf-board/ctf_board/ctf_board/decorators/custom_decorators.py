from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from challenges.models import CTFSettings
from ctf_board import settings


def delete_messages(function_to_decorate):
    def wrapper(*args, **kw):
        # Calling your function
        output = function_to_decorate(*args, **kw)
        # Below this line you can do post processing
        args[0].session['messages'] = []
        return output

    return wrapper


def delete_messages_before(rendered, request):
    request.session['messages'] = []
    return rendered


def ctf_running(function_to_decorate):
    def wrapper(request, *args, **kw):
        if request.user.is_staff or (CTFSettings.objects.first() and CTFSettings.objects.first().is_running):
            return function_to_decorate(request, *args, **kw)
        request.session['messages'] = ['Sorry the CTF is not running yet so you have to be a staff member to do this.']
        return redirect(reverse('team:login'))

    return wrapper


# def ctf_running():
#     def decorator(func):
#         @wraps(func, assigned=available_attrs(func))
#         def inner(request, *args, **kwargs):
#             if request.user.is_staff or (CTFSettings.objects.first() and CTFSettings.objects.first().is_running):
#                 return func(request, *args, **kwargs)
#             request.session['messages'] = ['Sorry the CTF is not running yet.']
#             return redirect(reverse('team:login'))
#         return inner
#     return decorator

def is_active(function_to_decorate):
    def wrapper(request, *args, **kw):
        if request.user.is_active or request.user.is_staff:
            return function_to_decorate(request, *args, **kw)
        request.session['messages'] = ['Sorry your account is not active yet, you should check your mails.']
        return redirect(reverse('team:profile'))

    return wrapper

