from .models import *
from .serializers import *
from rest_framework import viewsets, permissions
from rest_framework import serializers
from .models import *

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CategorySerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = BrandSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PermissionSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RoleSerializer


class InventoryProductViewSet(viewsets.ModelViewSet):
    queryset = InventoryProduct.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = InventoryProductSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class InventoryMovementViewSet(viewsets.ModelViewSet):
    queryset = InventoryMovement.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = InventoryMovementSerializer
