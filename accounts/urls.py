from django.urls import path
from . import views

urlpatterns = [
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('choice/', views.choice_view, name='choice'),
    path('register/', views.register_view, name='register'),
    path('register/student/', views.register_student_view, name='register_student'),
    path('register/instructor/', views.register_instructor_view, name='register_instructor'),
    path('register/employee/', views.register_employee_view, name='register_employee'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards
    path('dashboard/aluno/', views.aluno_dashboard, name='aluno_dashboard'),
    path('dashboard/instrutor/', views.instrutor_dashboard, name='instrutor_dashboard'),
    path('dashboard/funcionario/', views.funcionario_dashboard, name='funcionario_dashboard'),
    
    # Perfil
    path('profile/', views.profile_view, name='profile'),
]