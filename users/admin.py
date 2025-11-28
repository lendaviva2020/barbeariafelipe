from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "name", "get_is_active", "get_is_staff", "created_at")
    list_filter = ("created_at",)  # Removido is_active e is_staff pois são propriedades, não campos
    search_fields = ("email", "name", "phone")
    ordering = ("-created_at",)
    
    def get_is_active(self, obj):
        """Exibe is_active no admin"""
        return obj.is_active
    get_is_active.short_description = "Ativo"
    get_is_active.boolean = True
    
    def get_is_staff(self, obj):
        """Exibe is_staff no admin"""
        return obj.is_staff
    get_is_staff.short_description = "Staff"
    get_is_staff.boolean = True

    fieldsets = (
        (None, {"fields": ("email",)}),
        ("Informações Pessoais", {"fields": ("name", "phone", "avatar_url")}),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Datas", {"fields": ("created_at", "updated_at")}),
    )

    readonly_fields = ("created_at", "updated_at")

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "phone"),
            },
        ),
    )
