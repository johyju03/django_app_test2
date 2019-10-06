from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:  # 모델안의 모든 필드를 가져오도록 지정
        model = Product
        fields = '__all__'
