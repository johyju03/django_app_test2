### django_app_test2
DRF(Django Rest Framework) 및 Class 기반의 View를 적용시킨 테스트 웹 어플리케이션
***
- DRF(Django Rest Framework)
1. djangorestframework 플러그인설치
2. settings.py 내에 INSTALLED_APP 에 추가
```python
# 리스트 항목 조회
class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):  # 어떤 데이터를 가져올 것인지 명시
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# 단일 항목 조회
# mixins.RetrieveModelMixin 함수 사용 후, get 함수 사용시, 상세보기를 지원
class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):  # 어떤 데이터를 가져올 것인지 명시
        return Product.objects.all().order_by('id')  # url 에서 pk를 넘겨주게되면, 해당 내용에서 pk 에 해당하는 데이터를 걸러서준다.

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
```
- Class 기반 View (ex. 로그인 View)
```python
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
```
