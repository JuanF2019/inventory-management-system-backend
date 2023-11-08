# Create your views here.

from .models import *
from .serializers import *
from rest_framework import viewsets, permissions
from rest_framework import serializers
from rest_framework.permissions import DjangoModelPermissions
from .permissions import CustomDjangoModelPermissions

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [CustomDjangoModelPermissions]
    serializer_class = CategorySerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    permission_classes = [CustomDjangoModelPermissions]
    serializer_class = BrandSerializer

class InventoryProductViewSet(viewsets.ModelViewSet):
    queryset = InventoryProduct.objects.all()
    permission_classes = [CustomDjangoModelPermissions]
    serializer_class = InventoryProductSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [CustomDjangoModelPermissions]
    serializer_class = UserSerializer

class InventoryMovementViewSet(viewsets.ModelViewSet):
    queryset = InventoryMovement.objects.all()
    permission_classes = [CustomDjangoModelPermissions]
    serializer_class = InventoryMovementSerializer

