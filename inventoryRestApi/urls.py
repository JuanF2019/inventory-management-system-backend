from rest_framework import routers
from .api import *

router = routers.DefaultRouter()

router.register('api/categories',CategoryViewSet,'categories')
router.register('api/brands',BrandViewSet,'brands')
router.register('api/permissions',PermissionViewSet,'permission')
router.register('api/roles',RoleViewSet,'roles')
router.register('api/products',InventoryProductViewSet,'products')
router.register('api/users',UserViewSet,'users')
router.register('api/inventory-movements',InventoryMovementViewSet,'inventory-movements')

urlpatterns = router.urls
