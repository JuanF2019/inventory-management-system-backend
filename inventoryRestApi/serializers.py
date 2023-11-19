from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group
from datetime import datetime

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name')
        read_only_fields = ('id',)

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id','name')
        read_only_fields = ('id',)

class InventoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryProduct
        fields = ('code','name','description','dimensions','cost','sellingPrice','unitsAvailable','category','brand')
        read_only_fields = ()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name','document','doc_type','email','phone_number','birthday','password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        document = validated_data.pop('document')
        doc_type = validated_data.pop('doc_type')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        
        user = User.objects.create_user(email,password,document,doc_type,first_name,last_name)       

        if('phone_number' in validated_data.keys()): user.phone_number = validated_data.pop('phone_number')
        if('birthday' in validated_data.keys()): user.birthday = validated_data.pop('birthday')

        user.save(force_update=True)

        return user

    #called when patch??
    def update(self, instance, validated_data):
        keys = validated_data.keys()
        if('email' in keys): instance.email = validated_data.pop('email')
        if('password' in keys): instance.set_password(validated_data.pop('password'))
        if('document' in keys): instance.document = validated_data.pop('document')
        if('doc_type' in keys): instance.doc_type = validated_data.pop('doc_type')
        if('first_name' in keys): instance.first_name = validated_data.pop('first_name')
        if('last_name' in keys): instance.last_name = validated_data.pop('last_name')
        if('phone_number' in keys): instance.phone_number = validated_data.pop('phone_number')
        if('birthday' in keys): instance.birthday = validated_data.pop('birthday')

        instance.save()

        return instance


class InventoryMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryMovement
        fields = ('id', 'product','user','date','description','units','movType')
        read_only_fields = ('id',)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id','name')

class GroupIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id',)
