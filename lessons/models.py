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
    # Campos de localização baseados em CEP
    cep = models.CharField(max_length=9, verbose_name="CEP", blank=True)
    rua = models.CharField(max_length=255, verbose_name="Rua", blank=True)
    numero = models.CharField(max_length=10, verbose_name="Número")
    bairro = models.CharField(max_length=100, verbose_name="Bairro", blank=True)
    cidade = models.CharField(max_length=100, verbose_name="Cidade", blank=True)
    estado = models.CharField(max_length=2, verbose_name="Estado", blank=True)
    # Campo legado para compatibilidade
    location = models.CharField(max_length=255, blank=True)
    vehicle_type = models.CharField(max_length=1, choices=VEHICLE_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
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
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-time']
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
    
    def __str__(self):
        return f"Aula {self.lesson_number} - {self.student.full_name} com {self.instructor.full_name} em {self.date}"
