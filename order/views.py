from django.shortcuts import render, redirect
from .forms import OrderForm
from django.views.generic.edit import FormView
from django.views.generic import ListView
from .models import Order
from product.models import Product
from fcuser.models import Fcuser
from fcuser.decorators import login_required
from django.db import transaction
# 클래스 뷰의 경우, url을 통한 view 호출시, dispatch() 함수를 먼저 호출하기 때문에,
# 해당 함수에 데코레이터를 걸어야하지만, method_decorator 를 통하여, 아래와 같이 적용가능하다
from django.utils.decorators import method_decorator


# Create your views here.
@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView):
    form_class = OrderForm
    success_url = '/product/'

    def form_valid(self, form):
        with transaction.atomic():  # 트랜잭션 시작
            prod = Product.objects.get(pk=form.data.get('product'))
            order = Order(
                quantity=form.data.get('quantity'),
                product=Product.objects.get(pk=form.data.get('product')),
                fcuser=Fcuser.objects.get(email=self.request.session.get('user'))
            )
            order.save()
            prod.stock -= int(form.data.get('quantity'))
            prod.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('/product/' + str(form.data.get('product')))

    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request': self.request
        })
        return kw


@method_decorator(login_required, name='dispatch')
class OrderList(ListView):
    model = Order
    template_name = 'order.html'
    context_object_name = 'order_list'  # 지정시, html에서 받는 변수명이 object_list 에서 해당 이름으로 변경

    # 세션객체를 사용하여 필터를 하기위한 함수 (일반 queryset 은 세션객체를 못담음)
    def get_queryset(self, **kwargs):
        queryset = Order.objects.filter(fcuser__email=self.request.session.get('user'))
        return queryset
