from django.contrib import admin
from .models import Group, Profile, Tag, Student


# Register your models here.
# admin.site.register(Group)
# admin.site.register(Profile)
# admin.site.register(Tag)
# admin.site.register(Student)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "image", "status")
    list_filter = ("status",)
    search_fields = ("name", "email", "image", "status")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "middle_name", "last_name", "nickname", "birth_date", "age", "year", "photo", "description",
                    "group", "profile", "is_active", "created_at", "updated_at", "updated_at")
    list_filter = ("group", "year", "is_active",)
    search_fields = ("first_name", "middle_name", "last_name",)
