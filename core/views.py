from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from datetime import date, timedelta
from lessons.models import Lesson, StudentProgress


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
    
    # Weekly performance (last 7 days)
    week_data = []
    for i in range(7):
        day = today - timedelta(days=6-i)
        count = Lesson.objects.filter(
            instructor=request.user,
            date=day,
            status='completed'
        ).count()
        week_data.append({
            'day': day.strftime('%a')[:3],
            'count': count
        })
    
    context = {
        'stats': stats,
        'upcoming_lessons': upcoming_lessons,
        'week_data': week_data,
        'approval_rate': 92,  # This would be calculated from actual data
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
    
    # Get skills progress
    skills = StudentProgress.objects.filter(student=request.user)
    
    stats = {
        'upcoming_lessons': upcoming_lessons.count(),
        'total_hours': total_hours,
        'hours_left': max(0, required_hours - total_hours),
        'completed_lessons_count': completed_lessons.count(),
        'average_score': 8.5,  # Would be calculated from actual scores
    }
    
    context = {
        'stats': stats,
        'upcoming_lessons': upcoming_lessons,
        'completed_lessons': completed_lessons,
        'skills': skills,
        'total_hours': total_hours,
        'required_hours': required_hours,
        'progress_percentage': min(100, (total_hours / required_hours) * 100),
    }
    
    return render(request, 'core/aluno.html', context)


@login_required
def agendamento(request):
    """Lesson scheduling view"""
    from lessons.forms import LessonForm
    
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
    
    context = {
        'form': form,
        'instructors': instructors,
        'time_slots': ['08:00', '09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00'],
        'locations': [
            'Centro - Av. Principal, 123',
            'Zona Sul - Rua das Flores, 456',
            'Zona Norte - Av. Brasil, 789',
        ],
    }
    
    return render(request, 'core/agendamento.html', context)

