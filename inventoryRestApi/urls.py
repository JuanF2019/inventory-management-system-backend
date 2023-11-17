from rest_framework import routers
from .views import *
from django.urls import path

router = routers.DefaultRouter()

router.register('categories',CategoryViewSet,'categories')
router.register('brands',BrandViewSet,'brands')
router.register('products',InventoryProductViewSet,'products')
router.register('users',UserViewSet,'users')
  
urlpatterns = router.urls + [path('inventory-movements/',inventory_movement_create_list, name = "inventory-movement-create-list"),
                             path('inventory-movements/<int:id>', inventory_movement_update_detail_delete, name = "inventory-movement-update-detail-delete")]
