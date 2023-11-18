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
            serializer = InventoryMovementSerializer(data=request.data)

            if(not serializer.is_valid()):
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            updated_inv_mov = inv_mov_update(id,serializer) #serializer.save() is called internally     
            
            return Response(data=serializer.data,status=status.HTTP_200_OK) 

        if(request.method == 'GET'):
            inv_mov = inv_mov_detail(id)
            serializer = InventoryMovementSerializer(inv_mov)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
            
        if(request.method == 'DELETE'):
            deleted_inv_mov = inv_mov_delete(id)
            serializer = InventoryMovementSerializer(deleted_inv_mov)    
            return Response(data=serializer.data,status=status.HTTP_200_OK)
    
        return Response(data={"detail":f"Method {request.method} is not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)      
    except NotEnoughProductUnits as e:
        return Response(data={"detail": e.__str__()}, status=status.HTTP_409_CONFLICT) 
    except ObjectDoesNotExist as e:
        return Response(data={"detail": f"Inventory Movement with id {id} does not exists"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(data={"detail": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([CustomDjangoModelPermissions])
@api_view(['POST','GET'])
def inventory_movement_create_list(request):
    try:   
        if (request.method == 'POST'):
            serializer = InventoryMovementSerializer(data=request.data)

            if(not serializer.is_valid()):
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
                        
            inv_mov = inv_mov_create(serializer) #serializer.save() is called internally

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
        if (request.method == 'GET'):
            inv_movs = inv_mov_list()
            serializer = InventoryMovementSerializer(inv_movs, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)        

        return Response(data={"detail": f"Method {request.method} is not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    except Exception as e:
        return Response(data={"detail": f"{e.__str__()}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
