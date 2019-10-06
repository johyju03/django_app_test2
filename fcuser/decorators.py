from django.shortcuts import redirect
from fcuser.models import Fcuser


def login_required(function):
    def wrap(request, *args, **kwargs):  # dispatch 의 인자에 맞게 삽입
        user = request.session.get('user')
        if user is None or not user:
            return redirect('/login')
        return function(request, *args, **kwargs)

    return wrap


def admin_required(function):
    def wrap(request, *args, **kwargs):  # dispatch 의 인자에 맞게 삽입
        user = request.session.get('user')
        if user is None or not user:
            return redirect('/login')
        user = Fcuser.objects.get(email=user)
        if user.level != 'admin':
            return redirect('/')
        return function(request, *args, **kwargs)

    return wrap
