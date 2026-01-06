from django.urls import path
from . import views, api_views
from .delete_views import delete_account_view

urlpatterns = [
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('choice/', views.choice_view, name='choice'),
    path('register/', views.register_view, name='register'),
    path('register/student/', views.register_student_view, name='register_student'),
    path('register/instructor/', views.register_instructor_view, name='register_instructor'),
    path('register/employee/', views.register_employee_view, name='register_employee'),
    path('logout/', views.logout_view, name='logout'),
    
    # API REST
    path('api/register/instrutor/', api_views.register_api_instrutor, name='api_register_instrutor'),
    path('api/register/funcionario/', api_views.register_api_funcionario, name='api_register_funcionario'),
    path('api/register/aluno/', api_views.register_api_aluno, name='api_register_aluno'),
    path('api/login/', api_views.login_api, name='api_login'),
    path('api/me/', api_views.me_api, name='api_me'),
    path('api/logout/', api_views.logout_api, name='api_logout'),
    path('api/check-cpf/', api_views.check_cpf_api, name='api_check_cpf'),
    path('api/check-rg/', api_views.check_rg_api, name='api_check_rg'),
    
    # Dashboards
    path('dashboard/aluno/', views.aluno_dashboard, name='aluno_dashboard'),
    path('dashboard/instrutor/', views.instrutor_dashboard, name='instrutor_dashboard'),
    path('dashboard/funcionario/', views.funcionario_dashboard, name='funcionario_dashboard'),
    path('instructor/vehicle/', views.instructor_vehicle_view, name='instructor_vehicle'),
    
    # Perfil
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),

    # Exclusão de cadastro
    path('delete-account/', delete_account_view, name='delete_account'),
]