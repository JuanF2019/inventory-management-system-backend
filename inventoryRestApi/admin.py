from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import *

# Register your models here

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm

    ordering = ('email',)
    list_display = ("email","first_name","last_name",)

    fieldsets = (
        (None, {"fields": ("email", "password",)}),
        (("Personal info"), {"fields": ("first_name", "last_name",)}),
        (("Permissions"), {"fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),},),           
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name","document","doc_type","password1", "password2"),
            },
        ),
    )
    search_fields = ("document","email","first_name", "last_name",)

    def get_form(self,request,obj=None, **kwargs):
        form = super().get_form(request,obj,**kwargs)

        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['date_joined'].disabled = True
        return form

admin.site.register(User,CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(InventoryProduct)
admin.site.register(InventoryMovement)
