from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *

def undo_inv_movement(inv_movement,product, commit = False):
    units = inv_movement.units
    product.unitsAvailable += units if inv_movement.movType == "Salida" else -units
    if commit : product.save()
    return product

def inv_mov_update(request,inv_movement):
    new_inv_mov_data = request.data
    serializer = InventoryMovementSerializer(instance=inv_movement,data=new_inv_mov_data)

    if(not serializer.is_valid()):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #1. Deshacer el moviemiento que estaba hecho SIN guardar cambios
    prev_prod = inv_movement.product
    prev_prod = undo_inv_movement(inv_movement, prev_prod, commit = False)        

    #2. Verificar que la actualización es posible sin conflictos y actualizar la información del producto referenciado

    updated_inv_mov_data = serializer.validated_data
    updated_inv_mov_units = new_inv_mov_data['units']
    updated_inv_mov_type = new_inv_mov_data['movType']
    updated_inv_mov_product = InventoryProduct.objects.get(code=new_inv_mov_data['product'])

    if (prev_prod.code == updated_inv_mov_product.code):
        if (
            (updated_inv_mov_type == 'Entrada' and  prev_prod.unitsAvailable + updated_inv_mov_units < 0) #Entrada is checked because undo operation can lead to negative units
            or 
            (updated_inv_mov_type == 'Salida' and prev_prod.unitsAvailable - updated_inv_mov_units < 0)
        ):   
            return Response(data={"detail": f"Could not update, update results in negative available units for the referenced product"},status=status.HTTP_409_CONFLICT) 
        
        prev_prod.unitsAvailable += updated_inv_mov_units if updated_inv_mov_type == "Entrada" else -updated_inv_mov_units
        prev_prod.save()
        
    else:
        if(prev_prod.unitsAvailable < 0):
            return Response(data={"detail": f"Could not update, update results in negative available units for the referenced product prior to modification"},status=status.HTTP_409_CONFLICT) 
        if(updated_inv_mov_type == 'Salida' and updated_inv_mov_product.unitsAvailable - updated_inv_mov_units < 0):   
            return Response(data={"detail": f"Could not update, update results in negative available units for the new referenced product after modification"},status=status.HTTP_409_CONFLICT)       

        prev_prod.save()
        updated_inv_mov_product.unitsAvailable += updated_inv_mov_units if updated_inv_mov_type == "Entrada" else -updated_inv_mov_units
        updated_inv_mov_product.save()

    #3. Guardar la modificacion del movimiento
    serializer.save()
    return Response(data = serializer.data, status=status.HTTP_200_OK)
    
def inv_mov_detail(inv_mov):
    serializer = InventoryMovementSerializer(inv_mov)
    return Response(data=serializer.data,status=status.HTTP_200_OK)

def inv_mov_delete(inv_mov):
    prod = inv_mov.product
    undo_prod = undo_inv_movement(inv_mov,prod,commit=False)

    if(undo_prod.unitsAvailable < 0):
        return Response(data={"detail": f"Could not delete, deletion results in negative available units for the referenced product"},status=status.HTTP_409_CONFLICT) 
    
    undo_prod.save()
    inv_mov.delete()

    serializer = InventoryMovementSerializer(inv_mov)
    
    return Response(serializer.data,status=status.HTTP_200_OK)

def inv_mov_create(request):
    serializer = InventoryMovementSerializer(data=request.data)

    if(not serializer.is_valid()):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    val_data = serializer.validated_data

    prod_units = val_data['product'].unitsAvailable
    mov_units = val_data['units']
    mov_type = val_data['movType']

    if(mov_type == 'Entrada'):
        new_inv_mov = serializer.save()
        related_prod = new_inv_mov.product

        related_prod.unitsAvailable += new_inv_mov.units
        related_prod.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if(mov_type == 'Salida' and mov_units <= prod_units):
        new_inv_mov = serializer.save()
        related_prod = new_inv_mov.product

        related_prod.unitsAvailable -= new_inv_mov.units
        related_prod.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    return Response(data={"detail":"Available units for product are insufficient for request."},status=status.HTTP_409_CONFLICT)

def inv_mov_list():
    inv_movs = InventoryMovement.objects.all()
    serializer = InventoryMovementSerializer(inv_movs,many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)