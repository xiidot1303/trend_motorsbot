from rest_framework import serializers
from app.models import *

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class PassportDataSerializer(serializers.Serializer):
    serial = serializers.CharField()
    number = serializers.CharField()
    birth_date = serializers.CharField()

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"

class ProductIdSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()