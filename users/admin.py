from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ["email", "username", "first_name", "last_name", "phone_number", "avatar", "is_staff",
                    "is_superuser", "is_active"]
    search_fields = ["email", "username", "first_name", "last_name"]
    fieldsets = tuple(
        (
            name,
            {
                "fields": fields["fields"] + ("phone_number", "avatar",) if name == "Personal info" else fields[
                    "fields"],
                **{k: v for k, v in fields.items() if k != "fields"}
            }
        )
        for name, fields in UserAdmin.fieldsets
    )


admin.site.register(CustomUser, CustomUserAdmin)
