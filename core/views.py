from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Avg, Value
from django.db.models.functions import Replace, Coalesce
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
    
    # Calculate average rating
    avg_rating = monthly_lessons.aggregate(Avg('student_rating'))['student_rating__avg']
    
    stats = {
        'lessons_today': today_lessons.filter(status='scheduled').count(),
        'active_students': monthly_lessons.values('student').distinct().count(),
        'completed_lessons': monthly_lessons.filter(status='completed').count(),
        'hours_worked': monthly_lessons.filter(status='completed').count() * 50 // 60,  # Convert minutes to hours
        'average_rating': round(avg_rating, 1) if avg_rating else None,
    }
    
    # Get upcoming lessons (next 3 lessons)
    upcoming_lessons = Lesson.objects.filter(
        instructor=request.user,
        date__gte=today,
        status__in=['scheduled', 'in-progress']
    ).select_related('student').order_by('date', 'time')[:3]
    
    # Get pending lessons (awaiting instructor confirmation)
    pending_lessons = Lesson.objects.filter(
        instructor=request.user,
        status='pending'
    ).select_related('student').order_by('date', 'time')[:10]
    
    # Get recent rated lessons (with feedback from students)
    recent_ratings = Lesson.objects.filter(
        instructor=request.user,
        student_rating__isnull=False
    ).select_related('student').order_by('-updated_at')[:5]
    
    profile = request.user.get_profile()
    vehicles = profile.vehicles.all().order_by('-id') if profile else []
    selected_vehicle = None
    vehicle_param = request.GET.get('vehicle_id')
    if vehicle_param:
        selected_vehicle = vehicles.filter(id=vehicle_param).first()
    if not selected_vehicle:
        selected_vehicle = vehicles.first() if vehicles else None

    context = {
        'user': request.user,
        'profile': profile,
        'stats': stats,
        'upcoming_lessons': upcoming_lessons,
        'pending_lessons': pending_lessons,
        'recent_ratings': recent_ratings,
        'vehicles': vehicles,
        'selected_vehicle': selected_vehicle,
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
    
    # Get rejected lessons (awaiting reschedule) - excluding rescheduled ones
    rejected_lessons = Lesson.objects.filter(
        student=request.user,
        status='cancelled'
    ).order_by('-updated_at')[:5]
    
    # Get pending lessons (awaiting instructor confirmation)
    pending_lessons = Lesson.objects.filter(
        student=request.user,
        status='pending'
    ).order_by('-created_at')[:3]
    
    # Calculate progress
    total_hours = completed_lessons.count() * 50 // 60  # Convert to hours
    required_hours = 20
    
    # Get all instructors for reschedule modal
    from accounts.models import User
    instructors = User.objects.filter(role='instrutor', is_active=True).select_related('instructorprofile_profile')
    
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
        'rejected_lessons': rejected_lessons,
        'pending_lessons': pending_lessons,
        'total_hours': total_hours,
        'required_hours': required_hours,
        'progress_percentage': min(100, (total_hours / required_hours) * 100),
        'instructors': instructors,
    }
    
    return render(request, 'core/aluno.html', context)


@login_required
def agendamento(request):
    """Lesson scheduling view"""
    from lessons.forms import LessonForm
    from datetime import date
    from accounts.models import InstructorVehicle
    
    if request.method == 'POST':
        form = LessonForm(request.POST, student=request.user)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.student = request.user
            lesson.save()
            return redirect('aluno_dashboard')
    else:
        form = LessonForm(student=request.user)
    
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
    """API endpoint para filtrar instrutores por bairro/logradouro (ou CEP opcional), gênero e categoria de veículo"""
    from accounts.models import User

    bairro = request.GET.get('bairro', '').strip()
    rua = request.GET.get('rua', '').strip()
    gender = request.GET.get('gender', '')
    cep = request.GET.get('cep', '').strip()
    vehicle_type = request.GET.get('vehicle_type', '').strip()

    cep_digits = ''.join(filter(str.isdigit, cep))
    cep_prefix = cep_digits[:5] if len(cep_digits) >= 5 else ''

    if not bairro and not rua and not cep_prefix:
        return JsonResponse({'error': 'Informe bairro, logradouro ou CEP.'}, status=400)

    # Filtra instrutores ativos
    instructors_base = User.objects.filter(
        role='instrutor',
        is_active=True,
    ).exclude(
        instructorprofile_profile__status__in=['inativo', 'suspenso']
    ).select_related('instructorprofile_profile')

    # Filtra por gênero se fornecido
    if gender in ['M', 'F']:
        instructors_base = instructors_base.filter(instructorprofile_profile__gender=gender)

    # Filtra por categoria de veículo se fornecida
    if vehicle_type in ['A', 'B']:
        instructors_base = instructors_base.filter(
            Q(instructorprofile_profile__vehicle_categories='AB') |
            Q(instructorprofile_profile__vehicle_categories=vehicle_type)
        )

    # Combina filtros de endereço/CEP com OR para não excluir matches válidos
    address_filters = Q()
    if bairro:
        address_filters |= Q(instructorprofile_profile__address__icontains=bairro)
        address_filters |= Q(instructorprofile_profile__address_complement__icontains=bairro)
    if rua:
        address_filters |= Q(instructorprofile_profile__address__icontains=rua)
    if cep_prefix:
        address_filters |= Q(instructorprofile_profile__cep_base__startswith=cep_prefix)
        address_filters |= Q(instructorprofile_profile__cep__startswith=cep_prefix)

    if address_filters:
        instructors_base = instructors_base.filter(address_filters)

    instructors = instructors_base
    
    # Serializa resultados
    result = []
    for instructor in instructors[:20]:  # Máximo 20 instrutores
        profile = instructor.instructorprofile_profile
        # Calcula avaliação média a partir das aulas completadas
        avg_rating = instructor.instructor_lessons.filter(
            student_rating__isnull=False
        ).aggregate(Avg('student_rating'))['student_rating__avg']
        
        result.append({
            'id': instructor.id,
            'name': instructor.full_name,
            'gender': profile.get_gender_display() if profile.gender else 'Não informado',
            'gender_code': profile.gender,
            'gender_identity': profile.gender_identity,
            'gender_identity_label': profile.get_gender_identity_display() if profile.gender_identity else None,
            'rating': round(avg_rating, 1) if avg_rating else None,
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


@login_required
def submit_lesson_rating(request):
    """API endpoint para o aluno avaliar uma aula"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    import json
    
    try:
        data = json.loads(request.body)
        lesson_id = data.get('lesson_id')
        rating = data.get('rating')
        feedback = data.get('feedback', '')
        
        # Validações
        if not lesson_id:
            return JsonResponse({'error': 'ID da aula não fornecido'}, status=400)
        
        if not rating or not isinstance(rating, (int, float)):
            return JsonResponse({'error': 'Avaliação inválida'}, status=400)
        
        if rating < 1 or rating > 5:
            return JsonResponse({'error': 'Avaliação deve estar entre 1 e 5'}, status=400)
        
        # Busca a aula
        try:
            lesson = Lesson.objects.get(id=lesson_id, student=request.user)
        except Lesson.DoesNotExist:
            return JsonResponse({'error': 'Aula não encontrada'}, status=404)
        
        # Verifica se a aula foi completada
        if lesson.status != 'completed':
            return JsonResponse({'error': 'Apenas aulas completadas podem ser avaliadas'}, status=400)
        
        # Salva a avaliação
        lesson.student_rating = rating
        lesson.student_feedback = feedback
        lesson.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Avaliação enviada com sucesso!',
            'lesson_id': lesson.id,
            'rating': float(lesson.student_rating),
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def reschedule_lesson(request, lesson_id):
    """Endpoint para o aluno remarcar uma aula recusada"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    import json
    
    try:
        data = json.loads(request.body)
        new_date = data.get('date')
        new_time = data.get('time')
        new_instructor_id = data.get('instructor_id')
        
        # Busca a aula original (recusada)
        try:
            lesson = Lesson.objects.get(
                id=lesson_id,
                student=request.user,
                status='cancelled'
            )
        except Lesson.DoesNotExist:
            return JsonResponse({'error': 'Aula não encontrada ou já foi remarcada'}, status=404)
        
        # Validações de data e hora
        if not new_date or not new_time:
            return JsonResponse({'error': 'Data e hora são obrigatórios'}, status=400)
        
        # Atualiza a aula existente com os novos dados
        lesson.date = new_date
        lesson.time = new_time
        lesson.status = 'pending'  # Muda de 'cancelled' para 'pending'
        
        # Se um novo instrutor foi selecionado, atualizar
        if new_instructor_id:
            try:
                from accounts.models import User
                new_instructor = User.objects.get(id=new_instructor_id, role='instrutor')
                lesson.instructor = new_instructor
            except User.DoesNotExist:
                return JsonResponse({'error': 'Instrutor não encontrado'}, status=404)
        
        lesson.save()
        
        return JsonResponse({'success': True, 'message': 'Aula remarcada com sucesso'})
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def cancel_rejected_lesson(request, lesson_id):
    """Endpoint para o aluno cancelar definitivamente uma aula recusada"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        # Busca a aula recusada
        lesson = Lesson.objects.get(
            id=lesson_id,
            student=request.user,
            status='cancelled'
        )
        
        # Deleta a aula definitivamente
        lesson.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Aula cancelada definitivamente.'
        })
        
    except Lesson.DoesNotExist:
        return JsonResponse({'error': 'Aula não encontrada ou já foi processada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def cancel_lesson(request, lesson_id):
    """Endpoint genérico para o aluno cancelar qualquer aula (agendada, pendente, etc)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        # Busca a aula do aluno
        lesson = Lesson.objects.get(
            id=lesson_id,
            student=request.user
        )
        
        # Verifica se a aula pode ser cancelada (não pode cancelar aulas já completadas ou em andamento)
        if lesson.status in ['completed', 'in-progress']:
            return JsonResponse({'error': 'Esta aula não pode ser cancelada'}, status=400)
        
        # Deleta a aula definitivamente
        lesson.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Aula cancelada com sucesso.'
        })
        
    except Lesson.DoesNotExist:
        return JsonResponse({'error': 'Aula não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def instructor_cancel_lesson(request, lesson_id):
    """Endpoint para instrutor cancelar uma aula confirmada"""
    if request.user.role != 'instrutor':
        return JsonResponse({'error': 'Apenas instrutores podem cancelar aulas'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        # Busca a aula do instrutor
        lesson = Lesson.objects.get(
            id=lesson_id,
            instructor=request.user
        )
        
        # Verifica se a aula pode ser cancelada
        if lesson.status in ['completed', 'in-progress']:
            return JsonResponse({'error': 'Esta aula não pode ser cancelada'}, status=400)
        
        # Deleta a aula definitivamente
        lesson.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Aula cancelada com sucesso.'
        })
        
    except Lesson.DoesNotExist:
        return JsonResponse({'error': 'Aula não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def accept_lesson(request, lesson_id):
    """Endpoint para instrutor aceitar uma aula"""
    if request.user.role != 'instrutor':
        return JsonResponse({'error': 'Apenas instrutores podem aceitar aulas'}, status=403)
    
    try:
        lesson = Lesson.objects.get(id=lesson_id, instructor=request.user, status='pending')
        lesson.status = 'scheduled'
        lesson.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Aula confirmada com sucesso!',
            'lesson_id': lesson.id
        })
    except Lesson.DoesNotExist:
        return JsonResponse({'error': 'Aula não encontrada ou já foi processada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def reject_lesson(request, lesson_id):
    """Endpoint para instrutor recusar uma aula"""
    if request.user.role != 'instrutor':
        return JsonResponse({'error': 'Apenas instrutores podem recusar aulas'}, status=403)
    
    try:
        lesson = Lesson.objects.get(id=lesson_id, instructor=request.user, status='pending')
        lesson.status = 'cancelled'
        lesson.notes = f"Recusada pelo instrutor em {date.today().strftime('%d/%m/%Y')}"
        lesson.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Aula recusada',
            'lesson_id': lesson.id
        })
    except Lesson.DoesNotExist:
        return JsonResponse({'error': 'Aula não encontrada ou já foi processada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




