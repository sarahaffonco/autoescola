from django.urls import path
from . import views

urlpatterns = [
    path('', views.instrutor_dashboard, name='instrutor_dashboard'),
    path('aluno/', views.aluno_dashboard, name='aluno_dashboard'),
    path('agendamento/', views.agendamento, name='agendamento'),
    path('api/lookup-cep/', views.lookup_cep, name='lookup_cep'),
    path('api/filter-instructors/', views.filter_instructors, name='filter_instructors'),
    path('api/filter-vehicles/', views.filter_vehicles, name='filter_vehicles'),
]
