from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist
from .permissions import *
from .serializers import *
from .services import *
import datetime


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [CustomDjangoModelPermissions]
    serializer_class = CategorySerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    permission_classes = [CustomDjangoModelPermissions]
    serializer_class = BrandSerializer


class InventoryProductViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                              mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = InventoryProduct.objects.all()
    permission_classes = [CustomDjangoModelPermissions]
    serializer_class = InventoryProductSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [CustomDjangoModelPermissions]
    serializer_class = UserSerializer


@api_view(['PUT', 'GET', 'DELETE'])
@permission_classes([InventoryMovementPermissions, InventoryProductPermissions])
def inventory_movement_update_detail_delete(request, inv_mov_id):
    try:
        if request.method == 'PUT':
            serializer = InventoryMovementSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            inv_mov_update(inv_mov_id, serializer)  # serializer.save() is called internally

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        if request.method == 'GET':
            inv_mov = inv_mov_detail(inv_mov_id)
            serializer = InventoryMovementSerializer(inv_mov)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        if request.method == 'DELETE':
            deleted_inv_mov = inv_mov_delete(inv_mov_id)
            serializer = InventoryMovementSerializer(deleted_inv_mov)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data={"detail": f"Method {request.method} is not allowed"},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except NotEnoughProductUnits as e:
        return Response(data={"detail": e.__str__()}, status=status.HTTP_409_CONFLICT)
    except ObjectDoesNotExist:
        return Response(data={"detail": f"Inventory Movement with id {inv_mov_id} does not exists"},
                        status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(data={"detail": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST', 'GET'])
@permission_classes([InventoryMovementPermissions, InventoryProductPermissions])
def inventory_movement_create_list(request):
    try:
        if request.method == 'POST':
            serializer = InventoryMovementSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            inv_mov_create(serializer)  # serializer.save() is called internally

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'GET':
            inv_movs = inv_mov_list()
            serializer = InventoryMovementSerializer(inv_movs, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data={"detail": f"Method {request.method} is not allowed"},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    except Exception as e:
        return Response(data={"detail": f"{e.__str__()}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([GroupPermissions, UserPermissions])
def user_groups_list(request, user_document):
    try:
        if request.method == 'GET':
            user_groups = user_groups_list_service(user_document)

            serializer = GroupSerializer(user_groups, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data={"detail": f"Method {request.method} is not allowed"},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    except Exception as e:
        return Response(data={"detail": f"{e.__str__()}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'DELETE'])
@permission_classes([GroupPermissions, UserPermissions])
def user_groups_add_delete(request, user_document, group_id):
    try:
        if request.method == 'PUT':
            user_groups = user_groups_add(user_document, group_id)
            serializer = GroupSerializer(user_groups, many=True)

            return Response(data={"user_groups": serializer.data}, status=status.HTTP_200_OK)

        if request.method == 'DELETE':
            user_groups = user_groups_delete_service(user_document, group_id)
            serializer = GroupSerializer(user_groups, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data={"detail": f"Method {request.method} is not allowed"},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    except Exception as e:
        return Response(data={"detail": f"{e.__str__()}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([GroupPermissions])
def groups_list(request):
    try:
        if request.method == 'GET':
            groups = groups_list_service()
            serializer = GroupSerializer(groups, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data={"detail": f"Method {request.method} is not allowed"},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as e:
        return Response(data={"detail": f"{e.__str__()}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([CategoryPermissions, InventoryProductPermissions])
def graph_num_product_per_cat(request):
    try:
        if request.method == 'GET':
            data = graph_num_product_per_cat_service()

            return Response(data=data, status=status.HTTP_200_OK)

        return Response(data={"detail": f"Method {request.method} is not allowed"},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    except Exception as e:
        return Response(data={"detail": f"{e.__str__()}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([InventoryMovementPermissions])
def graph_movements_per_month(request):
    try:
        if request.method == 'GET':
            date_from, date_to = process_raw_date(
                request.query_params["date_from"],
                request.query_params["date_to"])

            data = graph_movements_per_month_service(date_from, date_to)

            return Response(data=data, status=status.HTTP_200_OK)

        return Response(data={"detail": f"Method {request.method} is not allowed"},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    except Exception as e:
        return Response(data={"detail": f"{e.__str__()}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([InventoryProductPermissions, InventoryProductPermissions])
def graph_value_per_month(request):
    try:
        if request.method == 'GET':
            date_from, date_to = process_raw_date(
                request.query_params["date_from"],
                request.query_params["date_to"])

            data = graph_value_per_month_service(date_from, date_to)

            return Response(data=data, status=status.HTTP_200_OK)

        return Response(data={"detail": f"Method {request.method} is not allowed"},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    except Exception as e:
        return Response(data={"detail": f"{e.__str__()}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def process_raw_date(date_from_raw, date_to_raw):
    date_format = '%d-%m-%Y'

    date_from = dt.strptime(date_from_raw, date_format).date()
    date_to = dt.strptime(date_to_raw, date_format).date()

    return date_from, date_to
