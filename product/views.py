from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .models import Product
from .forms import RegisterForm
from order.forms import OrderForm
from fcuser.decorators import admin_required
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework import mixins
from .serializers import ProductSerializer


# Create your views here.

# mixins.ListModelMixin 함수 사용 후, get 함수 사용시, list 형태를 지원
class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):  # 어떤 데이터를 가져올 것인지 명시
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# mixins.RetrieveModelMixin 함수 사용 후, get 함수 사용시, 상세보기를 지원
class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):  # 어떤 데이터를 가져올 것인지 명시
        return Product.objects.all().order_by('id')  # url 에서 pk를 넘겨주게되면, 해당 내용에서 pk 에 해당하는 데이터를 걸러서준다.

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list'  # 지정시, html에서 받는 변수명이 object_list 에서 해당 이름으로 변경


@method_decorator(admin_required, name='dispatch')
class ProductCreate(FormView):
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        product = Product(
            name=form.data.get('name'),
            price=form.data.get('price'),
            description=form.data.get('description'),
            stock=form.data.get('stock')
        )
        product.save()
        return super().form_valid(form)


class ProductDetail(DetailView):
    template_name = 'product_detail.html'
    queryset = Product.objects.all()
    context_object_name = 'product'

    # 기존 context 이외에 추가 데이터 전달이 필요한 경우
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = OrderForm(self.request)
        return context
