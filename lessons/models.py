from django.db import models
from django.conf import settings


class Lesson(models.Model):
    """Model for driving lessons"""
    STATUS_CHOICES = (
        ('pending', 'Pendente de Confirmação'),
        ('scheduled', 'Agendada'),
        ('in-progress', 'Em Andamento'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
        ('rescheduled', 'Remarcada'),
    )
    
    VEHICLE_TYPE_CHOICES = (
        ('A', 'Categoria A - Motocicleta'),
        ('B', 'Categoria B - Carro'),
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
        limit_choices_to={'role': 'instrutor'},
        null=True,
        blank=True,
        verbose_name='Instrutor'
    )
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField(default=50, help_text="Duração em minutos")
    # Campos de localização baseados em CEP
    cep = models.CharField(max_length=9, verbose_name="CEP", blank=True)
    rua = models.CharField(max_length=255, verbose_name="Rua", blank=True)
    numero = models.CharField(max_length=10, verbose_name="Número")
    bairro = models.CharField(max_length=100, verbose_name="Bairro", blank=True)
    cidade = models.CharField(max_length=100, verbose_name="Cidade", blank=True)
    estado = models.CharField(max_length=2, verbose_name="Estado", blank=True)
    # Campo legado para compatibilidade
    location = models.CharField(max_length=255, blank=True)
    vehicle_type = models.CharField(max_length=1, choices=VEHICLE_TYPE_CHOICES, null=True, blank=True, verbose_name='Tipo de Veículo')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    score = models.CharField(max_length=50, blank=True, help_text="Avaliação da aula")
    notes = models.TextField(blank=True)
    lesson_number = models.IntegerField(default=1)
    # Preferências do aluno
    prefer_adapted_pcd = models.BooleanField(default=False, verbose_name='Preferência: Adaptado PCD')
    prefer_dual_control = models.BooleanField(default=False, verbose_name='Preferência: Acionamento Duplo')
    # Veículo escolhido (opcional)
    vehicle = models.ForeignKey(
        'accounts.InstructorVehicle',
        on_delete=models.SET_NULL,
        related_name='lessons',
        null=True,
        blank=True,
        verbose_name='Veículo'
    )
    
    # Avaliação do aluno sobre o instrutor (1-5 estrelas)
    student_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name='Avaliação do Aluno',
        help_text='Nota de 1 a 5 estrelas dada pelo aluno'
    )
    # Feedback/comentário do aluno
    student_feedback = models.TextField(
        blank=True,
        verbose_name='Feedback do Aluno',
        help_text='Comentário do aluno sobre a aula'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-time']
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
    
    def __str__(self):
        return f"Aula {self.lesson_number} - {self.student.full_name} com {self.instructor.full_name} em {self.date}"
