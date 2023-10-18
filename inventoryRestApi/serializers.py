from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name')
        read_only_fields = ()


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id','name')
        read_only_fields = ()

class InventoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryProduct
        fields = ('code','name','description','dimensions','cost','sellingPrice','unitsAvailable','category','brand')
        read_only_fields = ()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','document','docType','email','phoneNumber','birthday')
        read_only_fields = ()


class InventoryMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryMovement
        fields = ('id', 'product','user','date','description','units','movType')
        read_only_fields = ()
