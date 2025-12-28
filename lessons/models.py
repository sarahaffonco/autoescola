from django.db import models
from django.conf import settings


class Lesson(models.Model):
    """Model for driving lessons"""
    STATUS_CHOICES = (
        ('scheduled', 'Agendada'),
        ('in-progress', 'Em Andamento'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    )
    
    VEHICLE_TYPE_CHOICES = (
        ('A', 'Categoria A - Motocicleta'),
        ('B', 'Categoria B - Carro'),
        ('D', 'Categoria D - Ônibus'),
    )
    
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_lessons',
        limit_choices_to={'role': 'aluno'}
    )
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='instructor_lessons',
        limit_choices_to={'role': 'instrutor'}
    )
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField(default=50, help_text="Duração em minutos")
    location = models.CharField(max_length=255)
    vehicle_type = models.CharField(max_length=1, choices=VEHICLE_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    score = models.CharField(max_length=50, blank=True, help_text="Avaliação da aula")
    notes = models.TextField(blank=True)
    lesson_number = models.IntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-time']
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
    
    def __str__(self):
        return f"Aula {self.lesson_number} - {self.student.full_name} com {self.instructor.full_name} em {self.date}"


class StudentProgress(models.Model):
    """Model to track student progress in different skills"""
    SKILL_CHOICES = (
        ('baliza', 'Baliza'),
        ('estacionamento', 'Estacionamento'),
        ('direcao_via', 'Direção em via'),
        ('conversoes', 'Conversões'),
        ('ladeira', 'Ladeira'),
    )
    
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progress',
        limit_choices_to={'role': 'aluno'}
    )
    skill = models.CharField(max_length=50, choices=SKILL_CHOICES)
    progress = models.IntegerField(default=0, help_text="Progresso de 0 a 100")
    
    class Meta:
        unique_together = ['student', 'skill']
        verbose_name = 'Progresso do Aluno'
        verbose_name_plural = 'Progressos dos Alunos'
    
    def __str__(self):
        return f"{self.student.full_name} - {self.get_skill_display()}: {self.progress}%"

