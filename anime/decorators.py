from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None

            if request.user.groups.exists():
                groups = request.user.groups.all()

            for group in groups:
                if group.name in allowed_roles:
                    return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorised to view this page")
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        if group == 'animeshnik':
            return redirect('home')
        if group == 'moderator':
            return redirect('home')
    return wrapper_func
