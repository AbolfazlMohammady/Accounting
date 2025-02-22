from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportMixin, ImportMixin 
from import_export import resources

from .models import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'phone', 'email', 'full_name', 'is_active', 'is_staff', 'date_joined')

@admin.register(User)
class CustomUserAdmin(ExportMixin, ImportMixin, UserAdmin):
    # resource_class = UserResource  
    fieldsets = (
        (None, {"fields": ("phone", 'email', "password",)}),
        (_("Personal info"), {"fields": ('full_name', 'age', 'bio', 'image',)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),

    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "password1", "password2"),
            },
        ),
    )
    list_display = ('id',"phone", "email", "full_name", "is_staff")
    search_fields = ("phone", "full_name", "email")
    ordering = ("phone",)


