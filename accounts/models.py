from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with role support"""
    ROLE_CHOICES = (
        ('instrutor', 'Instrutor'),
        ('funcionario', 'Funcionário'),
        ('aluno', 'Aluno'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='aluno')
    phone = models.CharField(max_length=20, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"{self.full_name or self.username} ({self.get_role_display()})"

