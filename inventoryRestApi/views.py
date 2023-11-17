# Create your views here.

from .models import *
from .serializers import *
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import DjangoModelPermissions
from .permissions import CustomDjangoModelPermissions
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist 
from .services import *

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

@permission_classes([CustomDjangoModelPermissions])
@api_view(['PUT','GET','DELETE'])
def inventory_movement_update_detail_delete(request, id):
    try:
        inv_movement = InventoryMovement.objects.get(id=id)#move this to services  
        if (request.method == 'PUT'):
            return inv_mov_update(request,inv_movement)
        if(request.method == 'GET'):
            return inv_mov_detail(inv_movement)
        if(request.method == 'DELETE'):
            return inv_mov_delete(inv_movement)

        return Response(data={"detail":f"Method {request.method} is not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)      
    except (ObjectDoesNotExist):
        return Response(data={"detail": f"Inventory Movement with id {id} does not exist."},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(data={"detail": f"{e.__str__()}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([CustomDjangoModelPermissions])
@api_view(['POST','GET'])
def inventory_movement_create_list(request):   
    if (request.method == 'POST'):
        return inv_mov_create(request)
    
    if (request.method == 'GET'):
        return inv_mov_list()

    return Response(data = {detail:f"Method {request.method} is not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class InventoryMovementViewSet(viewsets.ModelViewSet):
    queryset = InventoryMovement.objects.all()
    permission_classes = [CustomDjangoModelPermissions]
    serializer_class = InventoryMovementSerializer

