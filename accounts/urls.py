from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('choice/', views.choice_view, name='choice'),  # Nova rota
    path('register/', views.register_view, name='register'),  # Redireciona para choice
    path('register/student/', views.register_student_view, name='register_student'),
    path('register/instructor/', views.register_instructor_view, name='register_instructor'),
    path('register/employee/', views.register_employee_view, name='register_employee'),
    path('logout/', views.logout_view, name='logout'),
]