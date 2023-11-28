from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from .models import InventoryMovement, InventoryProduct, User, Category
from .exceptions import NotEnoughProductUnits
from .serializers import InventoryMovementSerializer, UserSerializer


def undo_inv_movement(inv_movement, product, commit=False):
    units = inv_movement.units
    product.unitsAvailable += units if inv_movement.movType == "Salida" else -units
    if commit: product.save()
    return product


def inv_mov_update(id, serializer):
    # 1. Deshacer el moviemiento que estaba hecho SIN guardar cambios
    inv_movement = inv_mov_detail(id)
    undone_prev_prod = undo_inv_movement(inv_movement, inv_movement.product, commit=False)

    # 2. Verificar que la actualización es posible sin conflictos y actualizar la información del producto referenciado
    updated_inv_mov_data = serializer.validated_data
    updated_inv_mov_units = updated_inv_mov_data['units']
    updated_inv_mov_type = updated_inv_mov_data['movType']
    updated_inv_mov_product = updated_inv_mov_data['product']

    if (undone_prev_prod.code == updated_inv_mov_product.code):
        if (
                (
                        updated_inv_mov_type == 'Entrada' and undone_prev_prod.unitsAvailable + updated_inv_mov_units < 0)  # Entrada is checked because undo operation can lead to negative units
                or
                (updated_inv_mov_type == 'Salida' and undone_prev_prod.unitsAvailable - updated_inv_mov_units < 0)
        ):
            raise NotEnoughProductUnits(
                "Not enough units available on the referenced product to update inventory movement")

        undone_prev_prod.unitsAvailable += updated_inv_mov_units if updated_inv_mov_type == "Entrada" else -updated_inv_mov_units
        undone_prev_prod.save()

    else:
        if (undone_prev_prod.unitsAvailable < 0):
            raise NotEnoughProductUnits(
                "Not enough units available on the currently referenced product to update inventory movement with new product")
        if (updated_inv_mov_type == 'Salida' and updated_inv_mov_product.unitsAvailable - updated_inv_mov_units < 0):
            raise NotEnoughProductUnits(
                "Not enough units available on the new referenced product to update inventory movement")

        undone_prev_prod.save()
        updated_inv_mov_product.unitsAvailable += updated_inv_mov_units if updated_inv_mov_type == "Entrada" else -updated_inv_mov_units
        updated_inv_mov_product.save()

    # 3. Actualizar el movimiento de inventario

    serializer.instance = inv_movement
    updated_inv_mov = serializer.save()

    return updated_inv_mov


def inv_mov_detail(id):
    return InventoryMovement.objects.get(id=id)


def inv_mov_delete(id):
    inv_mov = inv_mov_detail(id)
    prod = inv_mov.product
    undo_prod = undo_inv_movement(inv_mov, prod, commit=False)

    if (undo_prod.unitsAvailable < 0):
        raise NotEnoughProductUnits("Not enough units available on referenced product to delete inventory movement")

    undo_prod.save()
    inv_mov.delete()

    return inv_mov


def inv_mov_create(serializer: InventoryMovementSerializer):
    inv_mov_data = serializer.validated_data

    mov_units = inv_mov_data['units']
    mov_type = inv_mov_data['movType']

    related_prod = inv_mov_data['product']
    prod_units = related_prod.unitsAvailable

    if (not mov_type == 'Entrada' and not (mov_type == 'Salida' and mov_units <= prod_units)):
        raise NotEnoughProductUnits("Not enough units available on referenced product to create inventory movement")

    related_prod.unitsAvailable += mov_units if mov_type == 'Entrada' else -mov_units
    related_prod.save()
    inv_mov = serializer.save()

    return inv_mov


def inv_mov_list():
    return InventoryMovement.objects.all()


def user_groups_list_service(document):
    user = User.objects.get(document=document)
    return user.groups.all()


def user_groups_add(document, group_id):
    user = User.objects.get(document=document)
    group = Group.objects.get(id=group_id)
    user.groups.add(group)

    return user.groups.all()


def user_groups_delete_service(document, group_id):
    user = User.objects.get(document=document)
    group = Group.objects.get(id=group_id)
    user.groups.remove(group)

    return user.groups.all()


def groups_list_service():
    return Group.objects.all()


def graph_num_product_per_cat_service():
    categories = Category.objects.all()

    data_partial = {}

    for category in categories:
        data_partial[category.__str__()] = {"units": 0}

    products = InventoryProduct.objects.all()

    total_units = 0

    for product in products:
        data_partial[product.category.__str__()]["units"] += 1
        total_units += 1

    data = {"total_units": total_units, "data": []}

    for i in data_partial:
        units = data_partial[i]["units"]
        percentage = units / total_units
        data["data"].append({"category": i, "units": units, "percentage": percentage})

    return data
