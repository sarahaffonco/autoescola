from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, InstructorVehicle


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'full_name', 'role', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('role', 'phone', 'full_name')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('role', 'phone', 'full_name')}),
    )


@admin.register(InstructorVehicle)
class InstructorVehicleAdmin(admin.ModelAdmin):
    list_display = ['instructor', 'plate', 'make', 'model', 'year', 'dual_control', 'adapted_pcd']
    search_fields = ['plate', 'renavam', 'make', 'model', 'instructor__full_name']
    list_filter = ['dual_control', 'adapted_pcd', 'year']

