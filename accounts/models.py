from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import os
import re
import time
def upload_profile_photo(instance, filename):
    """Sanitize and standardize uploaded profile photo filenames.
    Generates: profiles/photos/user<id>_<timestamp>.<ext>
    """
    # Normalize filename to avoid hidden control chars/newlines that break media URLs
    base = os.path.basename(filename or '').strip()
    base = re.sub(r'\s+', '_', base)  # collapse spaces/newlines
    base = re.sub(r'[^A-Za-z0-9._-]', '', base)  # keep only safe chars

    # Extract extension safely
    ext = os.path.splitext(base)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        # Fallback to .jpg if unexpected (validation will also handle allowed types)
        ext = '.jpg'
    user_id = getattr(instance, 'user_id', None) or (getattr(instance, 'user', None) and instance.user.id) or 'unknown'
    safe_name = f"user{user_id}_{int(time.time())}{ext}"
    return os.path.join('profiles/photos/', safe_name)


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
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['-registration_date']
    
    def __str__(self):
        return f"{self.full_name or self.username} ({self.get_role_display()})"
    
    # Métodos utilitários
    def is_aluno(self):
        return self.role == 'aluno'
    
    def is_instrutor(self):
        return self.role == 'instrutor'
    
    def is_funcionario(self):
        return self.role == 'funcionario'
    
    def get_profile(self):
        """Retorna o perfil específico do usuário"""
        if self.is_aluno():
            return StudentProfile.objects.filter(user=self).first()
        elif self.is_instrutor():
            return InstructorProfile.objects.filter(user=self).first()
        elif self.is_funcionario():
            return EmployeeProfile.objects.filter(user=self).first()
        return None


# Validadores
def validate_image_extension(value):
    """Valida a extensão da imagem"""
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png']
    
    if ext not in valid_extensions:
        raise ValidationError('Formato de arquivo não suportado. Use apenas JPG, JPEG ou PNG.')


def validate_image_size(value):
    """Valida o tamanho da imagem (máximo 5MB)"""
    max_size = 5 * 1024 * 1024  # 5MB
    if value.size > max_size:
        raise ValidationError(f'A imagem é muito grande. Tamanho máximo: {max_size // (1024*1024)}MB')


def validate_document_size(value):
    """Valida o tamanho do documento (máximo 10MB)"""
    max_size = 10 * 1024 * 1024  # 10MB
    if value.size > max_size:
        raise ValidationError(f'O documento é muito grande. Tamanho máximo: {max_size // (1024*1024)}MB')


def validate_document_extension(value):
    """Valida a extensão do documento"""
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx']
    
    if ext not in valid_extensions:
        raise ValidationError('Formato de arquivo não suportado. Use apenas JPG, PNG, PDF, DOC ou DOCX.')


class BaseProfile(models.Model):
    """Classe base para perfis com campos comuns"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='%(class)s_profile')
    full_name = models.CharField(max_length=255, verbose_name="Nome Completo")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Telefone")
    birth_date = models.DateField(verbose_name="Data de Nascimento")
    photo = models.ImageField(
        upload_to=upload_profile_photo,
        verbose_name="Foto 3x4",
        validators=[validate_image_extension, validate_image_size]
    )
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    rg = models.CharField(max_length=20, verbose_name="RG")
    cep = models.CharField(max_length=9, verbose_name="CEP")
    address = models.CharField(max_length=255, verbose_name="Endereço")
    address_number = models.CharField(max_length=10, verbose_name="Número")
    address_complement = models.CharField(max_length=100, verbose_name="Complemento", blank=True)
    
    # Campos automáticos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ['full_name']
    
    def __str__(self):
        return f"{self.full_name}"
    
    def clean(self):
        """Validações comuns para todos os perfis"""
        super().clean()
        
        # Validação do CPF (11 dígitos)
        cpf_digits = ''.join(filter(str.isdigit, self.cpf))
        if len(cpf_digits) != 11:
            raise ValidationError({'cpf': 'CPF deve conter exatamente 11 dígitos'})
        
        # Validação do RG (8-20 caracteres)
        rg_clean = ''.join(filter(lambda x: x.isalnum() or x in '.-', self.rg))
        if len(rg_clean) < 8 or len(rg_clean) > 20:
            raise ValidationError({'rg': 'RG deve ter entre 8 e 20 caracteres válidos'})
        
        # Validação do CEP (8 dígitos)
        cep_digits = ''.join(filter(str.isdigit, self.cep))
        if len(cep_digits) != 8:
            raise ValidationError({'cep': 'CEP deve conter exatamente 8 dígitos'})
        
        # Validação da data de nascimento (não pode ser futura)
        from datetime import date
        if self.birth_date > date.today():
            raise ValidationError({'birth_date': 'Data de nascimento não pode ser futura'})
    
    def save(self, *args, **kwargs):
        self.clean()  # Executa validações antes de salvar
        super().save(*args, **kwargs)


class StudentProfile(BaseProfile):
    """Perfil específico para alunos"""
    GENDER_IDENTITY_CHOICES = (
        ('CF', 'Cisgênero Feminino'),
        ('CM', 'Cisgênero Masculino'),
        ('TM', 'Homem Transgênero'),
        ('TW', 'Mulher Transgênero'),
    )
    STATUS_CHOICES = (
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('pendente', 'Pendente'),
        ('suspenso', 'Suspenso'),
    )
    
    # Campos específicos do aluno
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='ativo',
        verbose_name="Status"
    )
    progress = models.IntegerField(
        default=0, 
        verbose_name="Progresso (%)",
        help_text="Progresso do aluno em porcentagem"
    )
    total_lessons = models.IntegerField(
        default=0, 
        verbose_name="Total de Aulas"
    )
    completed_lessons = models.IntegerField(
        default=0, 
        verbose_name="Aulas Concluídas"
    )
    enrollment_date = models.DateField(
        auto_now_add=True,
        verbose_name="Data de Matrícula"
    )
    observation = models.TextField(
        blank=True,
        verbose_name="Observações"
    )
    gender_identity = models.CharField(
        max_length=2,
        choices=GENDER_IDENTITY_CHOICES,
        verbose_name="Identidade de gênero",
        blank=True,
        help_text="Informação de identidade de gênero do aluno"
    )
    
    # Categoria de CNH que o aluno está tirando
    license_categories = models.CharField(
        max_length=2,
        choices=(
            ('A', 'Categoria A - Motocicleta'),
            ('B', 'Categoria B - Carro'),
            ('AB', 'Ambas as categorias'),
        ),
        default='B',
        verbose_name="Categoria(s) de CNH",
        help_text="Qual(is) categoria(s) de CNH o aluno está tirar"
    )
    
    # Documentos de suporte opcionais
    support_document_1 = models.FileField(
        upload_to='students/documents/',
        null=True,
        blank=True,
        verbose_name="Documento de Suporte 1",
        validators=[validate_document_extension, validate_document_size]
    )
    support_document_2 = models.FileField(
        upload_to='students/documents/',
        null=True,
        blank=True,
        verbose_name="Documento de Suporte 2",
        validators=[validate_document_extension, validate_document_size]
    )
    
    class Meta:
        verbose_name = "Perfil de Aluno"
        verbose_name_plural = "Perfis de Alunos"
    
    def clean(self):
        """Validações específicas para aluno"""
        super().clean()
        
        # Validação de idade mínima para aluno (18 anos)
        from datetime import date
        today = date.today()
        age = today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
        
        if age < 18:
            raise ValidationError({'birth_date': f'Aluno deve ter pelo menos 18 anos. Idade atual: {age} anos'})
        
        # Validação do progresso (0-100%)
        if self.progress < 0 or self.progress > 100:
            raise ValidationError({'progress': 'Progresso deve estar entre 0% e 100%'})
        
        # Validação das aulas
        if self.completed_lessons > self.total_lessons:
            raise ValidationError({'completed_lessons': 'Aulas concluídas não podem ser maiores que o total de aulas'})
    
    def update_progress(self):
        """Atualiza automaticamente o progresso baseado nas aulas"""
        if self.total_lessons > 0:
            self.progress = int((self.completed_lessons / self.total_lessons) * 100)
        else:
            self.progress = 0
        self.save()


class InstructorProfile(BaseProfile):
    """Perfil específico para instrutores"""
    STATUS_CHOICES = (
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('pendente', 'Pendente Aprovação'),
        ('suspenso', 'Suspenso'),
    )
    
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )
    GENDER_IDENTITY_CHOICES = (
        ('CF', 'Cisgênero Feminino'),
        ('CM', 'Cisgênero Masculino'),
        ('TM', 'Homem Transgênero'),
        ('TW', 'Mulher Transgênero'),
    )
    
    # Campos específicos do instrutor
    cnh = models.CharField(
        max_length=30, 
        verbose_name="Número da CNH"
    )
    cnh_emission_date = models.DateField(
        verbose_name="Data de Emissão da CNH"
    )
    cnh_document = models.FileField(
        upload_to='instructors/cnh/',
        verbose_name="CNH (Frente e Verso)",
        validators=[validate_document_extension, validate_document_size]
    )
    credential = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name="Credencial de Instrutor"
    )
    
    # Gênero para preferência do aluno
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name="Gênero",
        blank=True
    )
    gender_identity = models.CharField(
        max_length=2,
        choices=GENDER_IDENTITY_CHOICES,
        verbose_name="Identidade de gênero",
        blank=True,
        help_text="Usado para exibir e preferências; mapeado para Homem/Mulher."
    )
    
    # Localização do instrutor (para filtrar por proximidade)
    cep_base = models.CharField(
        max_length=9,
        verbose_name="CEP da Base/Garagem",
        blank=True,
        help_text="CEP onde o instrutor inicia as aulas"
    )
    
    # Categorias de veículos que o instrutor trabalha
    vehicle_categories = models.CharField(
        max_length=2,
        choices=(
            ('A', 'Categoria A - Motocicleta'),
            ('B', 'Categoria B - Carro'),
            ('AB', 'Ambas as categorias'),
        ),
        default='B',
        verbose_name="Categorias de Veículo",
        help_text="Qual(is) categoria(s) de veículo o instrutor trabalha"
    )

    def set_gender_from_identity(self):
        """Atualiza o campo binário `gender` com base na identidade."""
        if self.gender_identity in ('CF', 'TW'):
            self.gender = 'F'
        elif self.gender_identity in ('CM', 'TM'):
            self.gender = 'M'
    
    # Documentos de suporte opcionais
    support_document_1 = models.FileField(
        upload_to='instructors/documents/',
        null=True,
        blank=True,
        verbose_name="Documento de Suporte 1",
        validators=[validate_document_extension, validate_document_size]
    )
    support_document_2 = models.FileField(
        upload_to='instructors/documents/',
        null=True,
        blank=True,
        verbose_name="Documento de Suporte 2",
        validators=[validate_document_extension, validate_document_size]
    )
    
    # Status e métricas
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pendente',
        verbose_name="Status"
    )
    rating = models.FloatField(
        default=0.0,
        verbose_name="Avaliação",
        help_text="Avaliação média do instrutor (0-5)"
    )
    total_students = models.IntegerField(
        default=0, 
        verbose_name="Total de Alunos"
    )
    total_lessons = models.IntegerField(
        default=0, 
        verbose_name="Total de Aulas Ministradas"
    )
    hire_date = models.DateField(
        auto_now_add=True,
        verbose_name="Data de Contratação"
    )
    observation = models.TextField(
        blank=True,
        verbose_name="Observações"
    )
    
    class Meta:
        verbose_name = "Perfil de Instrutor"
        verbose_name_plural = "Perfis de Instrutores"
    
    def clean(self):
        """Validações específicas para instrutor"""
        super().clean()
        
        # Validação da CNH (mínimo 9 dígitos)
        cnh_digits = ''.join(filter(str.isdigit, self.cnh))
        if len(cnh_digits) < 9:
            raise ValidationError({'cnh': 'CNH deve conter pelo menos 9 dígitos'})
        
        # Validação da credencial (mínimo 5 caracteres)
        if len(self.credential.strip()) < 5:
            raise ValidationError({'credential': 'Credencial deve conter pelo menos 5 caracteres'})
        
        # Validação da data de emissão da CNH
        from datetime import date
        if self.cnh_emission_date > date.today():
            raise ValidationError({'cnh_emission_date': 'Data de emissão da CNH não pode ser futura'})
        
        if self.cnh_emission_date <= self.birth_date:
            raise ValidationError({'cnh_emission_date': 'Data de emissão da CNH deve ser posterior à data de nascimento'})
        
        # Validação da avaliação (0-5)
        if self.rating < 0 or self.rating > 5:
            raise ValidationError({'rating': 'Avaliação deve estar entre 0 e 5'})
    
    def calculate_rating(self, new_rating):
        """Calcula a nova avaliação média"""
        # Esta lógica seria implementada quando houver sistema de avaliações
        pass
    
    def is_approved(self):
        """Verifica se o instrutor está aprovado"""
        return self.status == 'ativo'


class InstructorVehicle(models.Model):
    """Informações do veículo associado ao instrutor"""
    instructor = models.OneToOneField(
        InstructorProfile,
        on_delete=models.CASCADE,
        related_name='vehicle',
        verbose_name="Instrutor"
    )

    plate = models.CharField(max_length=10, verbose_name="Placa")
    renavam = models.CharField(max_length=11, verbose_name="RENAVAM")
    last_license_exercise = models.DateField(
        verbose_name="Exercício do Último Licenciamento",
        null=True,
        blank=True,
    )
    model = models.CharField(max_length=100, verbose_name="Modelo")
    make = models.CharField(max_length=100, verbose_name="Marca")
    color = models.CharField(max_length=50, verbose_name="Cor")
    year = models.PositiveIntegerField(verbose_name="Ano")
    dual_control = models.BooleanField(default=False, verbose_name="Acionamento Duplo")
    adapted_pcd = models.BooleanField(default=False, verbose_name="Adaptado para PCD")

    class Meta:
        verbose_name = "Veículo do Instrutor"
        verbose_name_plural = "Veículos dos Instrutores"

    def __str__(self):
        return f"{self.plate} - {self.make} {self.model} ({self.year})"

    def clean(self):
        from datetime import date
        errors = {}

        # Validação de placa (formatos antigos e Mercosul). Permite hífen opcional e normaliza p/ maiúsculas.
        plate_raw = (self.plate or '').strip().upper()
        import re
        # Aceita AAA-1234, AAA1A23 e variações sem hífen
        pattern_old = re.compile(r'^[A-Z]{3}-?\d{4}$')
        pattern_mercosul = re.compile(r'^[A-Z]{3}-?[0-9][A-Z][0-9]{2}$')
        if not (pattern_old.match(plate_raw) or pattern_mercosul.match(plate_raw)):
            errors['plate'] = 'Placa inválida. Use formatos AAA-1234 ou ABC1D23.'
        else:
            self.plate = plate_raw.replace('-', '')  # Persistir sem hífen

        # RENAVAM: 11 dígitos numéricos
        ren = ''.join(filter(str.isdigit, self.renavam or ''))
        if len(ren) != 11:
            errors['renavam'] = 'RENAVAM deve conter exatamente 11 dígitos.'
        else:
            self.renavam = ren

        # Exercício do último licenciamento não pode ser futuro
        if self.last_license_exercise and self.last_license_exercise > date.today():
            errors['last_license_exercise'] = 'A data do último licenciamento não pode ser futura.'

        # Ano: razoável entre 1960 e ano atual + 1
        current_year = date.today().year
        if not self.year or self.year < 1960 or self.year > current_year + 1:
            errors['year'] = f"Ano deve estar entre 1960 e {current_year + 1}."

        # Campos de texto básicos
        if not (self.model or '').strip():
            errors['model'] = 'Informe o modelo do veículo.'
        if not (self.make or '').strip():
            errors['make'] = 'Informe a marca do veículo.'
        if not (self.color or '').strip():
            errors['color'] = 'Informe a cor do veículo.'

        if errors:
            raise ValidationError(errors)


class EmployeeProfile(BaseProfile):
    """Perfil específico para funcionários"""
    DEPARTMENT_CHOICES = (
        ('secretaria', 'Secretaria'),
        ('financeiro', 'Financeiro'),
        ('atendimento', 'Atendimento'),
        ('administrativo', 'Administrativo'),
        ('rh', 'Recursos Humanos'),
        ('outro', 'Outro'),
    )
    
    STATUS_CHOICES = (
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('ferias', 'Férias'),
        ('afastado', 'Afastado'),
        ('licenca', 'Licença'),
    )
    
    # Campos específicos do funcionário
    department = models.CharField(
        max_length=50, 
        choices=DEPARTMENT_CHOICES,
        verbose_name="Departamento"
    )
    position = models.CharField(
        max_length=100,
        verbose_name="Cargo"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='ativo',
        verbose_name="Status"
    )
    hire_date = models.DateField(
        auto_now_add=True,
        verbose_name="Data de Contratação"
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Salário"
    )
    observation = models.TextField(
        blank=True,
        verbose_name="Observações"
    )
    
    # Documentos de suporte opcionais
    support_document_1 = models.FileField(
        upload_to='employees/documents/',
        null=True,
        blank=True,
        verbose_name="Documento de Suporte 1",
        validators=[validate_document_extension, validate_document_size]
    )
    support_document_2 = models.FileField(
        upload_to='employees/documents/',
        null=True,
        blank=True,
        verbose_name="Documento de Suporte 2",
        validators=[validate_document_extension, validate_document_size]
    )
    
    class Meta:
        verbose_name = "Perfil de Funcionário"
        verbose_name_plural = "Perfis de Funcionários"
    
    def clean(self):
        """Validações específicas para funcionário"""
        super().clean()
        
        # Validação do cargo
        if len(self.position.strip()) < 2:
            raise ValidationError({'position': 'Cargo deve conter pelo menos 2 caracteres'})
        
        # Validação do salário (se informado)
        if self.salary and self.salary < 0:
            raise ValidationError({'salary': 'Salário não pode ser negativo'})
    
    def is_active_employee(self):
        """Verifica se o funcionário está ativo"""
        return self.status == 'ativo'