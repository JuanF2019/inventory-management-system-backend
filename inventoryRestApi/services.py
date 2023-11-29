import calendar
import datetime
from datetime import datetime as dt

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

    if undone_prev_prod.code == updated_inv_mov_product.code:
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
        if undone_prev_prod.unitsAvailable < 0:
            raise NotEnoughProductUnits(
                "Not enough units available on the currently referenced product to update inventory movement with new product")
        if updated_inv_mov_type == 'Salida' and updated_inv_mov_product.unitsAvailable - updated_inv_mov_units < 0:
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

    if undo_prod.unitsAvailable < 0:
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

    if not mov_type == 'Entrada' and not (mov_type == 'Salida' and mov_units <= prod_units):
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


def graph_movements_per_month_service(date_from: datetime.date, date_to: datetime.date):
    data = []
    month_date_points = define_month_start_end_points(date_from, date_to)

    for month in month_date_points:
        inv_movs = InventoryMovement.objects.filter(
            date__gte=month[0],
            date__lt=(month[1] + datetime.timedelta(days=1)))

        units_moved = 0
        units_in = 0
        units_out = 0

        for inv_mov in inv_movs:
            units = inv_mov.units
            units_moved += units
            if inv_mov.movType == InventoryMovement.MOV_TYPES[0][0]:
                units_in += units
            else:
                units_out += units

        data.append({"year": month[0].year, "month": month[0].month, "units_moved": units_moved, "units_in": units_in,
                     "units_out": units_out})

    return data


# revisar la fecha de creación del producto
def graph_value_per_month_service(date_from: datetime.date, date_to: datetime.date):
    data = []
    month_date_points = define_month_start_end_points(date_from, date_to)

    month = month_date_points[0]
    undone_products = undo_product_movements_until_date(month[0])
    undone_products = redo_inventory_movements_from_date_until_date(
        undone_products, month[0], month[1] + datetime.timedelta(days=1))
    data = append_total_month_value(data, undone_products, month[0])

    if len(month_date_points) > 1:
        for month in month_date_points[1:]:
            undone_products = redo_inventory_movements_from_date_until_date(
                undone_products, month[0], month[1] + datetime.timedelta(days=1))
            data = append_total_month_value(data, undone_products, month[0])
    return data


def append_total_month_value(data, undone_products, month: datetime.date):
    total_month_value = 0

    for product in undone_products.values():
        total_month_value += product.unitsAvailable * product.cost

    data.append({"year": month.year, "month": month.month, "inv_value": total_month_value})

    return data


def undo_product_movements_until_date(date: datetime.date):
    inv_movs = InventoryMovement.objects.filter(date__gte=date)
    products = {}

    for inv_mov in inv_movs:

        prod = inv_mov.product

        if prod.code in products:
            prod = products[prod.code]
        else:
            products[prod.code] = prod

        if inv_mov.movType == InventoryMovement.MOV_TYPES[0][0]:
            prod.unitsAvailable -= inv_mov.units
        else:
            prod.unitsAvailable += inv_mov.units

    return products


def redo_inventory_movements_from_date_until_date(undone_products, from_date: datetime.date, date_to: datetime.date):
    inv_movs = InventoryMovement.objects.filter(date__gte=from_date, date__lt=date_to)

    for inv_mov in inv_movs:

        prod_code = inv_mov.product.code

        if prod_code not in undone_products.keys():
            continue

        prod = undone_products[prod_code]

        if inv_mov.movType == InventoryMovement.MOV_TYPES[0][0]:
            prod.unitsAvailable += inv_mov.units
        else:
            prod.unitsAvailable -= inv_movs.units

    return undone_products


def define_month_start_end_points(date_from: datetime.date, date_to: datetime.date):
    month_start_end_points = []
    current_date = date_from

    while current_date <= date_to:
        year = current_date.year
        month = current_date.month
        month_start_date = datetime.date(year, month, current_date.day)
        month_end_date = datetime.date(year, month, calendar.monthrange(year, month)[1])
        month_start_end_points.append((month_start_date, month_end_date))
        current_date = add_one_month(current_date)

    return month_start_end_points


def add_one_month(date: datetime.date):
    days = calendar.monthrange(year=date.year, month=date.month)[1]
    return date + datetime.timedelta(days=days)
