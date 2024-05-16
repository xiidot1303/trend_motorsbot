from app.views import *
from app.services.product_service import *
from rest_framework import generics
from app.serializers import ProductListSerializer, ProductSerializer

class ProductListAPIView(generics.ListAPIView):
    queryset = product_list_all()
    serializer_class = ProductListSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = product_list_all()
    serializer_class = ProductSerializer
    lookup_field = 'id'