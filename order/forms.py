from django import forms



class OrderForm(forms.Form):
    # 세션객체를 넘기기위한 생성자 코드 수정
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    quantity = forms.IntegerField(
        error_messages={
            'required': '수량을 입력해주세요.'
        },
        label='수량'
    )

    product = forms.IntegerField(
        error_messages={
            'required': '상품설명을 입력해주세요.'
        },
        widget=forms.HiddenInput
    )

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')
        fcuser = self.request.session.get('user', None)

        if not (quantity and product and fcuser):
            self.add_error('quantity', '값이 없습니다.')
            self.add_error('product', '값이 없습니다.')
