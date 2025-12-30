from django.urls import path
from . import views

urlpatterns = [
    path('', views.instrutor_dashboard, name='instrutor_dashboard'),
    path('aluno/', views.aluno_dashboard, name='aluno_dashboard'),
    path('agendamento/', views.agendamento, name='agendamento'),
    path('api/lookup-cep/', views.lookup_cep, name='lookup_cep'),
    path('api/filter-instructors/', views.filter_instructors, name='filter_instructors'),
    path('api/filter-vehicles/', views.filter_vehicles, name='filter_vehicles'),
    path('api/submit-lesson-rating/', views.submit_lesson_rating, name='submit_lesson_rating'),
    path('api/accept-lesson/<int:lesson_id>/', views.accept_lesson, name='accept_lesson'),
    path('api/reject-lesson/<int:lesson_id>/', views.reject_lesson, name='reject_lesson'),
    path('api/reschedule-lesson/<int:lesson_id>/', views.reschedule_lesson, name='reschedule_lesson'),
    path('api/cancel-rejected-lesson/<int:lesson_id>/', views.cancel_rejected_lesson, name='cancel_rejected_lesson'),
    path('api/cancel-lesson/<int:lesson_id>/', views.cancel_lesson, name='cancel_lesson'),
]
