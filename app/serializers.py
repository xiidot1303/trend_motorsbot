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
        fields = ['id', 'title', 'region']

    def get_region_display(self, obj):
        return obj.get_region_display()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['region'] = instance.get_region_display()
        return representation

class ProductIdSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

class GetContractSerializer(serializers.Serializer):
    lead_id = serializers.IntegerField()
    contract = serializers.CharField()