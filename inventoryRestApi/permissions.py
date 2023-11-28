from rest_framework.permissions import DjangoModelPermissions
from django.contrib.auth.models import Group
from .models import User, InventoryMovement, InventoryProduct, Category


class CustomDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


# Taken from DjangoModelPermissions, except that model is specified without the queryset
def has_model_permissions(self, request, view, model_cls):
    # Workaround to ensure DjangoModelPermissions are not applied
    # to the root view when using DefaultRouter.
    if getattr(view, '_ignore_model_permissions', False):
        return True

    if not request.user or (
            not request.user.is_authenticated and self.authenticated_users_only):
        return False

    perms = self.get_required_permissions(request.method, model_cls)

    return request.user.has_perms(perms)


class GroupPermissions(CustomDjangoModelPermissions):
    def has_permission(self, request, view):
        print("Checked group permissions")
        return has_model_permissions(self, request, view, Group)


class UserPermissions(CustomDjangoModelPermissions):
    def has_permission(self, request, view):
        return has_model_permissions(self, request, view, User)


class InventoryMovementPermissions(CustomDjangoModelPermissions):
    def has_permission(self, request, view):
        return has_model_permissions(self, request, view, InventoryMovement)


class InventoryProductPermissions(CustomDjangoModelPermissions):
    def has_permission(self, request, view):
        return has_model_permissions(self, request, view, InventoryProduct)


class CategoryPermissions(CustomDjangoModelPermissions):
    def has_permission(self, request, view):
        return has_model_permissions(self, request, view, Category)
