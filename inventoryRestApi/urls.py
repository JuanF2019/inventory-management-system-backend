from rest_framework import routers
from .views import *
from django.urls import path

router = routers.DefaultRouter()

router.register('categories', CategoryViewSet, 'categories')
router.register('brands', BrandViewSet, 'brands')
router.register('products', InventoryProductViewSet, 'products')
router.register('users', UserViewSet, 'users')

urlpatterns = router.urls + [
    path('inventory-movements/', inventory_movement_create_list, name="inventory-movement-create-list"),
    path('inventory-movements/<int:inv_mov_id>/', inventory_movement_update_detail_delete,
         name="inventory-movement-update-detail-delete"),
    path('users/<str:user_document>/groups/', user_groups_list, name="user-groups-list-add"),
    path('users/<str:user_document>/groups/<int:group_id>/', user_groups_add_delete, name="user-groups-delete"),
    path('groups/', groups_list, name="groups-list"),

    path('graphs/num-products-per-category/', graph_num_product_per_cat, name="graph_product_per_cat"),
    path('graphs/movements-per-month/', graph_movements_per_month, name="graph_product_per_cat"),
    path('graphs/value-per-month/', graph_value_per_month, name="graph_product_per_cat")]
