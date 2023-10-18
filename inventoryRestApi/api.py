from .models import *
from .serializers import *
from rest_framework import viewsets, permissions
from rest_framework import serializers
from rest_framework.permissions import BasePermission, SAFE_METHODS, DjangoModelPermissions

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [DjangoModelPermissions]
    serializer_class = CategorySerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    permission_classes = [DjangoModelPermissions]
    serializer_class = BrandSerializer

class InventoryProductViewSet(viewsets.ModelViewSet):
    queryset = InventoryProduct.objects.all()
    permission_classes = [DjangoModelPermissions]
    serializer_class = InventoryProductSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [DjangoModelPermissions]
    serializer_class = UserSerializer

class InventoryMovementViewSet(viewsets.ModelViewSet):
    queryset = InventoryMovement.objects.all()
    permission_classes = [DjangoModelPermissions]
    serializer_class = InventoryMovementSerializer