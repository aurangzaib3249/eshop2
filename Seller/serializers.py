
from .models import *

from rest_framework.serializers import ModelSerializer


class StoreSerializer(ModelSerializer):
    class Meta:
        model=Store
        fields="__all__"
        
class ProductSerializer(ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"