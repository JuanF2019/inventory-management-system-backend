from rest_framework import routers
from .views import *
from django.urls import path

router = routers.DefaultRouter()

router.register('categories',CategoryViewSet,'categories')
router.register('brands',BrandViewSet,'brands')
router.register('products',InventoryProductViewSet,'products')
router.register('users',UserViewSet,'users')
router.register('inventory-movements',InventoryMovementViewSet,'inventory-movements')
  
urlpatterns = router.urls
