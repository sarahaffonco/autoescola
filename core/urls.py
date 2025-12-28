from django.urls import path
from . import views

urlpatterns = [
    path('', views.instrutor_dashboard, name='instrutor_dashboard'),
    path('aluno/', views.aluno_dashboard, name='aluno_dashboard'),
    path('agendamento/', views.agendamento, name='agendamento'),
]
