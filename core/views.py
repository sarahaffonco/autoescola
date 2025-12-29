from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse
from datetime import date, timedelta
from lessons.models import Lesson
import requests


@login_required
def instrutor_dashboard(request):
    """Instructor dashboard view"""
    if request.user.role != 'instrutor':
        return redirect('aluno_dashboard')
    
    today = date.today()
    this_month_start = today.replace(day=1)
    
    # Get lessons for today
    today_lessons = Lesson.objects.filter(
        instructor=request.user,
        date=today
    ).select_related('student')
    
    # Stats for the month
    monthly_lessons = Lesson.objects.filter(
        instructor=request.user,
        date__gte=this_month_start
    )
    
    stats = {
        'lessons_today': today_lessons.filter(status='scheduled').count(),
        'active_students': monthly_lessons.values('student').distinct().count(),
        'completed_lessons': monthly_lessons.filter(status='completed').count(),
        'hours_worked': monthly_lessons.filter(status='completed').count() * 50 // 60,  # Convert minutes to hours
    }
    
    # Get upcoming lessons (today and tomorrow)
    upcoming_lessons = Lesson.objects.filter(
        instructor=request.user,
        date__gte=today,
        date__lte=today + timedelta(days=1)
    ).select_related('student')[:4]
    
    context = {
        'user': request.user,
        'profile': request.user.get_profile(),
        'stats': stats,
        'upcoming_lessons': upcoming_lessons,
    }
    
    return render(request, 'core/instrutor.html', context)


@login_required
def aluno_dashboard(request):
    """Student dashboard view"""
    if request.user.role == 'instrutor':
        return redirect('instrutor_dashboard')
    
    # Get student's lessons
    completed_lessons = Lesson.objects.filter(
        student=request.user,
        status='completed'
    ).order_by('-date')[:4]
    
    upcoming_lessons = Lesson.objects.filter(
        student=request.user,
        date__gte=date.today(),
        status='scheduled'
    ).order_by('date', 'time').select_related('instructor')[:3]
    
    # Calculate progress
    total_hours = completed_lessons.count() * 50 // 60  # Convert to hours
    required_hours = 20
    
    stats = {
        'upcoming_lessons': upcoming_lessons.count(),
        'total_hours': total_hours,
        'hours_left': max(0, required_hours - total_hours),
        'completed_lessons_count': completed_lessons.count(),
    }
    
    context = {
        'user': request.user,
        'profile': request.user.get_profile(),
        'stats': stats,
        'upcoming_lessons': upcoming_lessons,
        'completed_lessons': completed_lessons,
        'total_hours': total_hours,
        'required_hours': required_hours,
        'progress_percentage': min(100, (total_hours / required_hours) * 100),
    }
    
    return render(request, 'core/aluno.html', context)


@login_required
def agendamento(request):
    """Lesson scheduling view"""
    from lessons.forms import LessonForm
    from datetime import date
    from accounts.models import InstructorVehicle
    
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.student = request.user
            lesson.save()
            return redirect('aluno_dashboard')
    else:
        form = LessonForm()
    
    # Get available instructors
    from accounts.models import User
    instructors = User.objects.filter(role='instrutor', is_active=True)
    # Lista de veículos disponíveis (de instrutores ativos)
    vehicles = InstructorVehicle.objects.select_related('instructor').filter(instructor__user__is_active=True)
    
    context = {
        'form': form,
        'instructors': instructors,
        'vehicles': vehicles,
        'time_slots': ['08:00', '09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00'],
        'locations': [
            'Centro - Av. Principal, 123',
            'Zona Sul - Rua das Flores, 456',
            'Zona Norte - Av. Brasil, 789',
        ],
        'today': date.today(),
        'profile': request.user.get_profile(),
    }
    
    return render(request, 'core/agendamento.html', context)


@login_required
def lookup_cep(request):
    """API endpoint para buscar endereço pelo CEP"""
    cep = request.GET.get('cep', '').strip()
    
    if not cep or len(cep.replace('-', '')) != 8:
        return JsonResponse({'error': 'CEP inválido'}, status=400)
    
    # Formata o CEP
    cep_formatted = cep.replace('-', '')
    cep_display = f"{cep_formatted[:5]}-{cep_formatted[5:]}"
    
    try:
        # Usa a API ViaCEP para buscar o endereço
        response = requests.get(f'https://viacep.com.br/ws/{cep_formatted}/json/', timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if 'erro' in data:
            return JsonResponse({'error': 'CEP não encontrado'}, status=404)
        
        return JsonResponse({
            'success': True,
            'cep': cep_display,
            'rua': data.get('logradouro', ''),
            'bairro': data.get('bairro', ''),
            'cidade': data.get('localidade', ''),
            'estado': data.get('uf', ''),
        })
    except requests.RequestException as e:
        return JsonResponse({'error': f'Erro ao buscar CEP: {str(e)}'}, status=500)


def filter_instructors(request):
    """API endpoint para filtrar instrutores por CEP e gênero"""
    from accounts.models import InstructorProfile, User
    
    cep = request.GET.get('cep', '').strip()
    gender = request.GET.get('gender', '')
    
    if not cep or len(cep.replace('-', '')) != 8:
        return JsonResponse({'error': 'CEP inválido'}, status=400)
    
    # Remove formatação do CEP
    cep_clean = cep.replace('-', '')
    
    # Filtra instrutores ativos
    instructors_base = User.objects.filter(
        role='instrutor',
        is_active=True,
    ).exclude(instructorprofile_profile__status__in=['inativo', 'suspenso'])
    instructors_base = instructors_base.select_related('instructorprofile_profile')
    
    # Filtra por gênero se fornecido
    if gender in ['M', 'F']:
        instructors_base = instructors_base.filter(instructorprofile_profile__gender=gender)
    
    # Filtra por proximidade de CEP (simples: mesmo 5 primeiros dígitos ou CEP exato)
    # Uma implementação mais robusta usaria GeoDjango
    if cep_clean:
        cep_prefix = cep_clean[:5]
        nearby = instructors_base.filter(instructorprofile_profile__cep_base__startswith=cep_prefix)
        no_cep = instructors_base.filter(instructorprofile_profile__cep_base='')
        instructors = (nearby | no_cep).distinct()
    else:
        instructors = instructors_base
    
    # Serializa resultados
    result = []
    for instructor in instructors[:20]:  # Máximo 20 instrutores
        profile = instructor.instructorprofile_profile
        result.append({
            'id': instructor.id,
            'name': instructor.full_name,
            'gender': profile.get_gender_display() if profile.gender else 'Não informado',
            'gender_code': profile.gender,
            'gender_identity': profile.gender_identity,
            'gender_identity_label': profile.get_gender_identity_display() if profile.gender_identity else None,
            'rating': profile.rating,
            'vehicle_id': profile.vehicle.id if profile.vehicle else None,
        })
    
    return JsonResponse({'instructors': result})


def filter_vehicles(request):
    """API endpoint para filtrar veículos por instrutor e preferências"""
    from accounts.models import InstructorVehicle
    
    instructor_id = request.GET.get('instructor_id')
    vehicle_type = request.GET.get('vehicle_type', '')
    prefer_dual = request.GET.get('prefer_dual') == 'true'
    prefer_pcd = request.GET.get('prefer_pcd') == 'true'
    
    if not instructor_id:
        return JsonResponse({'error': 'Instrutor não especificado'}, status=400)
    
    try:
        # Filtra veículos do instrutor específico
        vehicles = InstructorVehicle.objects.filter(
            instructor__user_id=instructor_id
        )
        
        # Filtra por tipo de veículo (categoria A, B, D)
        # Por enquanto, apenas retorna o veículo do instrutor
        # se tiver múltiplos, podem ser filtrados aqui
        
        result = []
        for vehicle in vehicles:
            item = {
                'id': vehicle.id,
                'plate': vehicle.plate,
                'make': vehicle.make,
                'model': vehicle.model,
                'year': vehicle.year,
                'dual_control': vehicle.dual_control,
                'adapted_pcd': vehicle.adapted_pcd,
                'display': f"{vehicle.make} {vehicle.model} ({vehicle.year})"
            }
            
            # Filtra por preferências se especificadas
            if prefer_dual and not vehicle.dual_control:
                continue
            if prefer_pcd and not vehicle.adapted_pcd:
                continue
            
            result.append(item)
        
        return JsonResponse({'vehicles': result})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




