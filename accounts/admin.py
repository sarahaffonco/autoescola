from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, InstructorVehicle, InstructorProfile, StudentProfile


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


@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'status', 'gender', 'vehicle_categories', 'rating']
    list_filter = ['status', 'gender', 'vehicle_categories']
    search_fields = ['full_name', 'cpf', 'user__username']
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('user', 'full_name', 'email', 'phone', 'cpf', 'rg', 'birth_date', 'photo')
        }),
        ('Endereço', {
            'fields': ('cep', 'address', 'address_number', 'address_complement')
        }),
        ('Credenciais CNH', {
            'fields': ('cnh', 'cnh_emission_date', 'cnh_document', 'credential')
        }),
        ('Gênero e Identidade', {
            'fields': ('gender', 'gender_identity')
        }),
        ('Localização e Categorias', {
            'fields': ('cep_base', 'vehicle_categories')
        }),
        ('Status e Métricas', {
            'fields': ('status', 'rating', 'total_students', 'total_lessons', 'observation')
        }),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'status', 'license_categories', 'progress']
    list_filter = ['status', 'license_categories']
    search_fields = ['full_name', 'cpf', 'user__username']
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('user', 'full_name', 'email', 'phone', 'cpf', 'rg', 'birth_date', 'photo')
        }),
        ('Endereço', {
            'fields': ('cep', 'address', 'address_number', 'address_complement')
        }),
        ('CNH e Progresso', {
            'fields': ('license_categories', 'progress', 'total_lessons', 'completed_lessons')
        }),
        ('Gênero e Identidade', {
            'fields': ('gender_identity',)
        }),
        ('Status', {
            'fields': ('status', 'enrollment_date', 'observation')
        }),
    )


@admin.register(InstructorVehicle)
class InstructorVehicleAdmin(admin.ModelAdmin):
    list_display = ['instructor', 'plate', 'make', 'model', 'year', 'dual_control', 'adapted_pcd']
    search_fields = ['plate', 'renavam', 'make', 'model', 'instructor__full_name']
    list_filter = ['dual_control', 'adapted_pcd', 'year']
