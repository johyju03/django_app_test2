from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password
from .models import Fcuser


# Create your views here.
def index(request):
    return render(request, 'index.html', {'email': request.session.get('user')})


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'  # POST 성공시 이동할 URL

    # clean 이후 저장
    def form_valid(self, form):
        fcuser = Fcuser(
            email=form.data.get('email'),
            password=make_password(form.data.get('password')),
            level='user'
        )
        fcuser.save()

        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):  # 유효성 검사(forms.py의 clean 함수)가 끝났을 때 실행
        self.request.session['user'] = form.data.get('email')
        # 오버라이딩 했기 때문에, 부모 메소드를 다시 호출
        return super().form_valid(form)


def logout(request):
    if 'user' in request.session:
        del (request.session['user'])
    return redirect('/')
