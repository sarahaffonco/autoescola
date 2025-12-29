from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from datetime import date, timedelta
import re
from .models import User, StudentProfile, InstructorProfile, EmployeeProfile, InstructorVehicle


class BaseRegistrationForm(UserCreationForm):
    """Formulário base para registro de todos os tipos de usuários"""
    
    # Campos básicos que todos os usuários têm
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'seu@email.com'})
    )
    
    full_name = forms.CharField(
        max_length=255,
        required=True,
        label='Nome Completo',
        widget=forms.TextInput(attrs={'placeholder': 'Seu nome completo'})
    )
    
    phone = forms.CharField(
        max_length=20,
        required=True,
        label='Telefone',
        widget=forms.TextInput(attrs={'placeholder': '(00) 00000-0000'})
    )
    
    birth_date = forms.DateField(
        required=True,
        label='Data de Nascimento',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    photo = forms.ImageField(
        required=True,
        label='Foto 3x4',
        help_text='JPG, JPEG ou PNG (máximo 5MB)'
    )
    
    # Documentos
    cpf = forms.CharField(
        max_length=14,
        required=True,
        label='CPF',
        widget=forms.TextInput(attrs={'placeholder': '000.000.000-00'})
    )
    
    rg = forms.CharField(
        max_length=20,
        required=True,
        label='RG',
        widget=forms.TextInput(attrs={'placeholder': '00.000.000-0'})
    )
    
    # Endereço
    cep = forms.CharField(
        max_length=9,
        required=True,
        label='CEP',
        widget=forms.TextInput(attrs={'placeholder': '00000-000'})
    )
    
    address = forms.CharField(
        required=True,
        label='Endereço',
        widget=forms.TextInput(attrs={'placeholder': 'Rua, número, bairro, cidade'})
    )
    
    address_number = forms.CharField(
        required=True,
        label='Número',
        widget=forms.TextInput(attrs={'placeholder': 'Número'})
    )
    
    address_complement = forms.CharField(
        required=False,
        label='Complemento',
        widget=forms.TextInput(attrs={'placeholder': 'Complemento (opcional)'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nome de usuário'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes CSS para validação
        for field_name, field in self.fields.items():
            if hasattr(field, 'widget') and field.widget:
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'
    
    # ============================================
    # VALIDAÇÕES COMUNS
    # ============================================
    
    def clean_email(self):
        """Valida que o email é único"""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError('Este email já está cadastrado')
        return email
    
    def clean_cpf(self):
        """Valida e formata o CPF"""
        cpf = self.cleaned_data.get('cpf', '')
        
        # Remove tudo que não é número
        cpf_numeros = ''.join(filter(str.isdigit, cpf))
        
        # Validação de tamanho
        if len(cpf_numeros) != 11:
            raise ValidationError('CPF deve conter exatamente 11 dígitos numéricos')
        
        # Validação do CPF usando algoritmo oficial
        if not self.validar_cpf(cpf_numeros):
            raise ValidationError('CPF inválido')
        
        # Formata para o padrão 000.000.000-00
        cpf_formatado = f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"
        
        # Verifica se já existe no banco de dados
        if (StudentProfile.objects.filter(cpf=cpf_formatado).exists() or
            InstructorProfile.objects.filter(cpf=cpf_formatado).exists() or
            EmployeeProfile.objects.filter(cpf=cpf_formatado).exists()):
            raise ValidationError('Este CPF já está cadastrado no sistema')
        
        return cpf_formatado
    
    def clean_rg(self):
        """Valida e formata o RG"""
        rg = self.cleaned_data.get('rg', '')
        
        # Remove espaços extras
        rg = rg.strip()
        
        # Remove caracteres indesejados, mantendo apenas letras, números, pontos e hífens
        rg_limpo = re.sub(r'[^A-Za-z0-9.-]', '', rg)
        
        # Validação de tamanho
        if len(rg_limpo) < 8 or len(rg_limpo) > 20:
            raise ValidationError('RG deve ter entre 8 e 20 caracteres válidos')
        
        return rg_limpo
    
    def clean_cep(self):
        """Valida e formata o CEP"""
        cep = self.cleaned_data.get('cep', '')
        
        # Remove tudo que não é número
        cep_numeros = ''.join(filter(str.isdigit, cep))
        
        # Validação de tamanho
        if len(cep_numeros) != 8:
            raise ValidationError('CEP deve conter exatamente 8 dígitos numéricos')
        
        # Formata para o padrão 00000-000
        return f"{cep_numeros[:5]}-{cep_numeros[5:]}"
    
    def clean_photo(self):
        """Valida a foto"""
        photo = self.cleaned_data.get('photo')
        if photo:
            # Validação do tipo de arquivo
            valid_extensions = ['.jpg', '.jpeg', '.png']
            if not any(photo.name.lower().endswith(ext) for ext in valid_extensions):
                raise ValidationError('Apenas arquivos JPG, JPEG e PNG são permitidos.')
            
            # Validação do tamanho do arquivo
            max_size = 5 * 1024 * 1024  # 5MB
            if photo.size > max_size:
                raise ValidationError(f'A foto deve ter no máximo {max_size // (1024*1024)}MB')
        
        return photo
    
    def clean_birth_date(self):
        """Valida a data de nascimento"""
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            today = date.today()
            age = today.year - birth_date.year - (
                (today.month, today.day) < (birth_date.month, birth_date.day)
            )
            
            # Verifica se a data não é futura
            if birth_date > today:
                raise ValidationError('Data de nascimento não pode ser futura')
        
        return birth_date
    
    @staticmethod
    def validar_cpf(cpf):
        """Valida o CPF usando o algoritmo oficial"""
        # Remove caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, cpf))
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verifica se é uma sequência de números iguais
        if cpf == cpf[0] * len(cpf):
            return False
        
        # Calcula o primeiro dígito verificador
        soma = 0
        peso = 10
        for i in range(9):
            soma += int(cpf[i]) * peso
            peso -= 1
        
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        if digito1 != int(cpf[9]):
            return False
        
        # Calcula o segundo dígito verificador
        soma = 0
        peso = 11
        for i in range(10):
            soma += int(cpf[i]) * peso
            peso -= 1
        
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        if digito2 != int(cpf[10]):
            return False
        
        return True


class StudentRegistrationForm(BaseRegistrationForm):
    """Formulário específico para alunos"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].help_text = 'Você deve ter pelo menos 18 anos para se cadastrar'
    
    def clean_birth_date(self):
        """Valida que o aluno tem pelo menos 18 anos"""
        birth_date = super().clean_birth_date()
        
        if birth_date:
            today = date.today()
            age = today.year - birth_date.year - (
                (today.month, today.day) < (birth_date.month, birth_date.day)
            )
            
            # Validação de idade mínima para aluno
            min_age = 18
            if age < min_age:
                raise ValidationError(f'Para se cadastrar como aluno, é necessário ter pelo menos {min_age} anos. Você tem {age} anos.')
        
        return birth_date
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'aluno'
        
        if commit:
            user.save()
            
            # Cria o perfil do aluno
            StudentProfile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone'],
                birth_date=self.cleaned_data['birth_date'],
                photo=self.cleaned_data['photo'],
                cpf=self.cleaned_data['cpf'],
                rg=self.cleaned_data['rg'],
                cep=self.cleaned_data['cep'],
                address=self.cleaned_data['address'],
                address_number=self.cleaned_data['address_number'],
                address_complement=self.cleaned_data.get('address_complement', ''),
                # Campos específicos do aluno
                status='ativo',
                progress=0,
                total_lessons=0,
                completed_lessons=0
            )
        
        return user


class InstructorRegistrationForm(BaseRegistrationForm):
    """Formulário específico para instrutores"""
    
    # Campos específicos de instrutor
    cnh = forms.CharField(
        max_length=30,
        required=True,
        label='Número da CNH',
        widget=forms.TextInput(attrs={'placeholder': 'Digite o número da CNH'})
    )
    
    cnh_emission_date = forms.DateField(
        required=True,
        label='Data de Emissão da CNH',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    credential = forms.CharField(
        max_length=100,
        required=True,
        label='Credencial de Instrutor',
        widget=forms.TextInput(attrs={'placeholder': 'Número da credencial'})
    )
    
    cnh_document = forms.FileField(
        required=True,
        label='CNH (Frente e Verso)',
        help_text='JPG, PNG ou PDF (máximo 10MB)'
    )
    
    # Documentos de suporte opcionais
    support_document_1 = forms.FileField(
        required=False,
        label='Documento de Suporte 1',
        help_text='Comprovante de residência, etc. (opcional)'
    )
    
    support_document_2 = forms.FileField(
        required=False,
        label='Documento de Suporte 2',
        help_text='Certificado de curso, etc. (opcional)'
    )

    # Veículo do instrutor
    vehicle_plate = forms.CharField(
        max_length=10,
        required=True,
        label='Placa do Veículo',
        widget=forms.TextInput(attrs={'placeholder': 'ABC1D23 ou AAA-1234'})
    )
    vehicle_renavam = forms.CharField(
        max_length=11,
        required=True,
        label='RENAVAM',
        widget=forms.TextInput(attrs={'placeholder': '11 dígitos'})
    )
    vehicle_model = forms.CharField(
        max_length=100,
        required=True,
        label='Modelo',
        widget=forms.TextInput(attrs={'placeholder': 'Ex.: Onix 1.0'})
    )
    vehicle_make = forms.CharField(
        max_length=100,
        required=True,
        label='Marca',
        widget=forms.TextInput(attrs={'placeholder': 'Ex.: Chevrolet'})
    )
    vehicle_color = forms.CharField(
        max_length=50,
        required=True,
        label='Cor',
        widget=forms.TextInput(attrs={'placeholder': 'Ex.: Prata'})
    )
    vehicle_year = forms.IntegerField(
        required=True,
        label='Ano',
        widget=forms.NumberInput(attrs={'placeholder': 'Ex.: 2022', 'min': 1960})
    )
    vehicle_dual_control = forms.BooleanField(
        required=False,
        label='Possui acionamento duplo (pedais no passageiro)'
    )
    vehicle_adapted_pcd = forms.BooleanField(
        required=False,
        label='Veículo adaptado para PCD'
    )
    
    def clean_cnh(self):
        """Valida o número da CNH"""
        cnh = self.cleaned_data.get('cnh', '')
        cnh_numeros = ''.join(filter(str.isdigit, cnh))
        
        if len(cnh_numeros) < 9:
            raise ValidationError('CNH deve conter pelo menos 9 dígitos')
        
        return cnh
    
    def clean_credential(self):
        """Valida a credencial"""
        credential = self.cleaned_data.get('credential', '').strip()
        if len(credential) < 5:
            raise ValidationError('Credencial deve conter pelo menos 5 caracteres')
        return credential
    
    def clean_cnh_emission_date(self):
        """Valida a data de emissão da CNH"""
        emission_date = self.cleaned_data.get('cnh_emission_date')
        birth_date = self.cleaned_data.get('birth_date')
        
        if emission_date and birth_date:
            # Valida que a data de emissão é posterior à data de nascimento
            if emission_date <= birth_date:
                raise ValidationError('Data de emissão da CNH deve ser posterior à data de nascimento')
            
            # Valida que a data de emissão não é futura
            today = date.today()
            if emission_date > today:
                raise ValidationError('Data de emissão da CNH não pode ser futura')
        
        return emission_date
    
    def clean_cnh_document(self):
        """Valida o documento da CNH"""
        cnh_doc = self.cleaned_data.get('cnh_document')
        if cnh_doc:
            # Validação do tipo de arquivo
            valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
            if not any(cnh_doc.name.lower().endswith(ext) for ext in valid_extensions):
                raise ValidationError('Apenas arquivos JPG, JPEG, PNG e PDF são permitidos para a CNH.')
            
            # Validação do tamanho do arquivo
            max_size = 10 * 1024 * 1024  # 10MB
            if cnh_doc.size > max_size:
                raise ValidationError(f'O documento da CNH deve ter no máximo {max_size // (1024*1024)}MB')
        
        return cnh_doc

    # ==========================
    # Validações do veículo
    # ==========================
    def clean_vehicle_plate(self):
        plate = (self.cleaned_data.get('vehicle_plate') or '').strip().upper()
        import re
        pattern_old = re.compile(r'^[A-Z]{3}-?\d{4}$')
        pattern_mercosul = re.compile(r'^[A-Z]{3}-?[0-9][A-Z][0-9]{2}$')
        if not (pattern_old.match(plate) or pattern_mercosul.match(plate)):
            raise ValidationError('Placa inválida. Use AAA-1234 ou ABC1D23.')
        return plate.replace('-', '')

    def clean_vehicle_renavam(self):
        ren = ''.join(filter(str.isdigit, self.cleaned_data.get('vehicle_renavam') or ''))
        if len(ren) != 11:
            raise ValidationError('RENAVAM deve conter exatamente 11 dígitos.')
        return ren

    def clean_vehicle_year(self):
        from datetime import date
        year = self.cleaned_data.get('vehicle_year')
        current_year = date.today().year
        if not year or year < 1960 or year > current_year + 1:
            raise ValidationError(f"Ano deve estar entre 1960 e {current_year + 1}.")
        return year
    
    def clean_support_document_1(self):
        """Valida documento de suporte 1"""
        return self._validate_support_document(self.cleaned_data.get('support_document_1'), 'Documento de Suporte 1')
    
    def clean_support_document_2(self):
        """Valida documento de suporte 2"""
        return self._validate_support_document(self.cleaned_data.get('support_document_2'), 'Documento de Suporte 2')
    
    def _validate_support_document(self, document, field_name):
        """Validação genérica para documentos de suporte"""
        if document:
            # Validação do tipo de arquivo
            valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx']
            if not any(document.name.lower().endswith(ext) for ext in valid_extensions):
                raise ValidationError(f'Apenas arquivos JPG, JPEG, PNG, PDF, DOC e DOCX são permitidos para {field_name}.')
            
            # Validação do tamanho do arquivo
            max_size = 10 * 1024 * 1024  # 10MB
            if document.size > max_size:
                raise ValidationError(f'{field_name} deve ter no máximo {max_size // (1024*1024)}MB')
        
        return document
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'instrutor'
        
        if commit:
            user.save()
            
            # Cria o perfil do instrutor
            profile = InstructorProfile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone'],
                birth_date=self.cleaned_data['birth_date'],
                photo=self.cleaned_data['photo'],
                cpf=self.cleaned_data['cpf'],
                rg=self.cleaned_data['rg'],
                cep=self.cleaned_data['cep'],
                address=self.cleaned_data['address'],
                address_number=self.cleaned_data['address_number'],
                address_complement=self.cleaned_data.get('address_complement', ''),
                # Campos específicos do instrutor
                cnh=self.cleaned_data['cnh'],
                cnh_emission_date=self.cleaned_data['cnh_emission_date'],
                cnh_document=self.cleaned_data['cnh_document'],
                credential=self.cleaned_data['credential'],
                support_document_1=self.cleaned_data.get('support_document_1'),
                support_document_2=self.cleaned_data.get('support_document_2'),
                status='pendente',  # Aguarda aprovação
                rating=0.0,
                total_students=0,
                total_lessons=0
            )

            # Cria o veículo associado
            InstructorVehicle.objects.create(
                instructor=profile,
                plate=self.cleaned_data['vehicle_plate'],
                renavam=self.cleaned_data['vehicle_renavam'],
                model=self.cleaned_data['vehicle_model'],
                make=self.cleaned_data['vehicle_make'],
                color=self.cleaned_data['vehicle_color'],
                year=self.cleaned_data['vehicle_year'],
                dual_control=self.cleaned_data.get('vehicle_dual_control', False),
                adapted_pcd=self.cleaned_data.get('vehicle_adapted_pcd', False),
            )
        
        return user


class EmployeeRegistrationForm(BaseRegistrationForm):
    """Formulário específico para funcionários"""
    
    # Campos específicos de funcionário
    department = forms.ChoiceField(
        required=True,
        label='Departamento',
        choices=[
            ('', 'Selecione um departamento'),
            ('secretaria', 'Secretaria'),
            ('financeiro', 'Financeiro'),
            ('atendimento', 'Atendimento'),
            ('administrativo', 'Administrativo'),
            ('rh', 'Recursos Humanos'),
            ('outro', 'Outro'),
        ]
    )
    
    position = forms.CharField(
        max_length=100,
        required=True,
        label='Cargo',
        widget=forms.TextInput(attrs={'placeholder': 'Seu cargo'})
    )
    
    def clean_department(self):
        """Valida o departamento"""
        department = self.cleaned_data.get('department')
        if not department:
            raise ValidationError('Selecione um departamento')
        return department
    
    def clean_position(self):
        """Valida o cargo"""
        position = self.cleaned_data.get('position', '').strip()
        if len(position) < 2:
            raise ValidationError('Cargo deve conter pelo menos 2 caracteres')
        return position
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'funcionario'
        
        if commit:
            user.save()
            
            # Cria o perfil do funcionário
            EmployeeProfile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone'],
                birth_date=self.cleaned_data['birth_date'],
                photo=self.cleaned_data['photo'],
                cpf=self.cleaned_data['cpf'],
                rg=self.cleaned_data['rg'],
                cep=self.cleaned_data['cep'],
                address=self.cleaned_data['address'],
                address_number=self.cleaned_data['address_number'],
                address_complement=self.cleaned_data.get('address_complement', ''),
                # Campos específicos do funcionário
                department=self.cleaned_data['department'],
                position=self.cleaned_data['position'],
                status='ativo',
                is_active=True
            )
        
        return user


class UserLoginForm(forms.Form):
    """Formulário de login com validações específicas"""
    
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'seu@email.com'})
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
        required=True,
        label='Senha'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove a validação automática do Django para poder customizar
        self.error_messages = {
            'email_not_found': 'Email não encontrado. Verifique se digitou corretamente.',
            'incorrect_password': 'Senha incorreta. Tente novamente.',
            'inactive_account': 'Sua conta está inativa. Entre em contato com o administrador.',
        }
    
    def clean_email(self):
        """Valida se o email existe no sistema"""
        email = self.cleaned_data.get('email')
        
        if email:
            try:
                user = User.objects.get(email=email)
                
                # Verifica se o usuário está ativo
                if not user.is_active:
                    raise ValidationError(self.error_messages['inactive_account'])
                
            except User.DoesNotExist:
                # Salva o erro no campo email
                self.add_error('email', self.error_messages['email_not_found'])
        
        return email
    
    def clean(self):
        """Validação cruzada de email e senha"""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        # Se o email não existe, já paramos aqui
        if self.errors.get('email'):
            return cleaned_data
        
        # Se temos email e senha, valida a senha
        if email and password:
            try:
                user = User.objects.get(email=email)
                
                # Verifica a senha
                if not user.check_password(password):
                    # Adiciona erro específico no campo password
                    self.add_error('password', self.error_messages['incorrect_password'])
                
            except User.DoesNotExist:
                # Isso não deveria acontecer se clean_email() passou
                pass
        
        return cleaned_data


# Formulário simplificado para a view genérica (não será mais usado diretamente)
class UserRegistrationForm(BaseRegistrationForm):

    """Formulário genérico para registro (mantido para compatibilidade)"""
    
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=True,
        label='Tipo de Conta'
    )
    
    class Meta(BaseRegistrationForm.Meta):
        fields = BaseRegistrationForm.Meta.fields + ['role']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        
        if commit:
            user.save()
            
            # Cria o perfil apropriado baseado no role
            if user.role == 'aluno':
                StudentProfile.objects.create(
                    user=user,
                    full_name=self.cleaned_data['full_name'],
                    email=self.cleaned_data['email'],
                    phone=self.cleaned_data['phone'],
                    birth_date=self.cleaned_data['birth_date'],
                    photo=self.cleaned_data['photo'],
                    cpf=self.cleaned_data['cpf'],
                    rg=self.cleaned_data['rg'],
                    cep=self.cleaned_data['cep'],
                    address=self.cleaned_data['address'],
                    address_number=self.cleaned_data['address_number'],
                    address_complement=self.cleaned_data.get('address_complement', ''),
                    status='ativo',
                    progress=0,
                    total_lessons=0,
                    completed_lessons=0
                )
            elif user.role == 'instrutor':
                # Para instrutor, alguns campos serão None
                InstructorProfile.objects.create(
                    user=user,
                    full_name=self.cleaned_data['full_name'],
                    email=self.cleaned_data['email'],
                    phone=self.cleaned_data['phone'],
                    birth_date=self.cleaned_data['birth_date'],
                    photo=self.cleaned_data['photo'],
                    cpf=self.cleaned_data['cpf'],
                    rg=self.cleaned_data['rg'],
                    cep=self.cleaned_data['cep'],
                    address=self.cleaned_data['address'],
                    address_number=self.cleaned_data['address_number'],
                    address_complement=self.cleaned_data.get('address_complement', ''),
                    status='pendente',
                    is_active=True,
                    rating=0.0,
                    total_students=0,
                    total_lessons=0
                )
            elif user.role == 'funcionario':
                EmployeeProfile.objects.create(
                    user=user,
                    full_name=self.cleaned_data['full_name'],
                    email=self.cleaned_data['email'],
                    phone=self.cleaned_data['phone'],
                    birth_date=self.cleaned_data['birth_date'],
                    photo=self.cleaned_data['photo'],
                    cpf=self.cleaned_data['cpf'],
                    rg=self.cleaned_data['rg'],
                    cep=self.cleaned_data['cep'],
                    address=self.cleaned_data['address'],
                    address_number=self.cleaned_data['address_number'],
                    address_complement=self.cleaned_data.get('address_complement', ''),
                    status='ativo',
                    is_active=True
                )
        
        return user
    
class StudentEditForm(forms.ModelForm):
    """Formulário para edição de aluno"""
    
    class Meta:
        model = StudentProfile
        fields = [
            'full_name', 'email', 'phone', 'birth_date',
            'cpf', 'rg', 'cep', 'address', 'address_number', 'address_complement',
            'photo'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'photo': forms.FileInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Torna o CPF somente leitura (não pode ser alterado)
        self.fields['cpf'].widget.attrs['readonly'] = True
        self.fields['cpf'].widget.attrs['class'] = 'bg-gray-100 cursor-not-allowed'
        
        # Adiciona classes CSS
        for field_name, field in self.fields.items():
            if field.widget:
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'


class InstructorEditForm(forms.ModelForm):
    """Formulário para edição de instrutor"""
    
    class Meta:
        model = InstructorProfile
        fields = [
            'full_name', 'email', 'phone', 'birth_date',
            'cep', 'address', 'address_number', 'address_complement',
            'photo'  # Apenas a foto pode ser alterada
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'photo': forms.FileInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adiciona classes CSS aos campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all'
        
        # Torna campos obrigatórios
        self.fields['full_name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['birth_date'].required = True
        self.fields['cep'].required = True
        self.fields['address'].required = True
        self.fields['address_number'].required = True
        
        # Adiciona classes CSS
        for field_name, field in self.fields.items():
            if field.widget:
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'


class InstructorPersonalEditForm(forms.Form):
    """Formulário simplificado para edição de dados pessoais do instrutor"""
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Nome de Usuário',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome de usuário',
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all'
        })
    )
    
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'seu@email.com',
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all'
        })
    )
    
    password = forms.CharField(
        required=False,
        label='Nova Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Deixe em branco para manter a senha atual',
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all'
        }),
        help_text='Deixe em branco se não quiser alterar a senha'
    )
    
    password_confirm = forms.CharField(
        required=False,
        label='Confirme a Nova Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme a nova senha',
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all'
        })
    )
    
    photo = forms.ImageField(
        required=False,
        label='Foto 3x4',
        help_text='JPG, JPEG ou PNG (máximo 5MB)',
        widget=forms.FileInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border-2 border-dashed border-gray-300 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all',
            'accept': 'image/jpeg,image/jpg,image/png'
        })
    )
    
    def __init__(self, *args, user=None, profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.profile = profile
        
        # Preenche os valores iniciais
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
    
    def clean_username(self):
        """Valida que o username é único"""
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise ValidationError('Este nome de usuário já está em uso')
        return username
    
    def clean_email(self):
        """Valida que o email é único"""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise ValidationError('Este email já está cadastrado')
        return email
    
    def clean(self):
        """Valida que as senhas coincidem"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password != password_confirm:
            raise ValidationError('As senhas não coincidem')
        
        return cleaned_data
    
    def save(self):
        """Salva as alterações no User e no Profile"""
        # Atualiza o User
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']
        
        # Atualiza a senha se fornecida
        if self.cleaned_data.get('password'):
            self.user.set_password(self.cleaned_data['password'])
        
        self.user.save()
        
        # Atualiza a foto no profile se fornecida
        if self.cleaned_data.get('photo'):
            # Se não existe perfil, cria um vazio (instructor sem dados completos)
            if not self.profile:
                birth_date = date.today() - timedelta(days=365*18)  # 18 anos atrás
                self.profile = InstructorProfile.objects.create(
                    user=self.user,
                    full_name=self.user.full_name or self.user.username,
                    email=self.user.email,
                    phone=self.user.phone or '',
                    birth_date=birth_date,
                    cpf='00000000000',  # CPF mínimo obrigatório
                    rg='00000000',  # RG mínimo obrigatório
                    cep='00000000',  # CEP mínimo obrigatório
                    address='Não informado',
                    address_number='0',
                    cnh='00000000000',  # CNH mínimo obrigatório
                    cnh_emission_date=date.today(),
                    credential='TEMP00',  # Credencial mínima obrigatória (5+ caracteres)
                )
            
            self.profile.photo = self.cleaned_data['photo']
            self.profile.save()
        
        return self.user


class StudentPersonalEditForm(forms.Form):
    """Formulário simplificado para edição de dados pessoais do aluno"""
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Nome de Usuário',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome de usuário',
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all'
        })
    )
    
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'seu@email.com',
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all'
        })
    )
    
    password = forms.CharField(
        required=False,
        label='Nova Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Deixe em branco para manter a senha atual',
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all'
        }),
        help_text='Deixe em branco se não quiser alterar a senha'
    )
    
    password_confirm = forms.CharField(
        required=False,
        label='Confirme a Nova Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme a nova senha',
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all'
        })
    )
    
    photo = forms.ImageField(
        required=False,
        label='Foto 3x4',
        help_text='JPG, JPEG ou PNG (máximo 5MB)',
        widget=forms.FileInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border-2 border-dashed border-gray-300 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all',
            'accept': 'image/jpeg,image/jpg,image/png'
        })
    )
    
    def __init__(self, *args, user=None, profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.profile = profile
        
        # Preenche os valores iniciais
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
    
    def clean_username(self):
        """Valida que o username é único"""
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise ValidationError('Este nome de usuário já está em uso')
        return username
    
    def clean_email(self):
        """Valida que o email é único"""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise ValidationError('Este email já está cadastrado')
        return email
    
    def clean(self):
        """Valida que as senhas coincidem"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password != password_confirm:
            raise ValidationError('As senhas não coincidem')
        
        return cleaned_data
    
    def save(self):
        """Salva as alterações no User e no Profile"""
        # Atualiza o User
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']
        
        # Atualiza a senha se fornecida
        if self.cleaned_data.get('password'):
            self.user.set_password(self.cleaned_data['password'])
        
        self.user.save()
        
        # Atualiza a foto no profile se fornecida
        if self.cleaned_data.get('photo'):
            # Se não existe perfil, cria um vazio (student sem dados completos)
            if not self.profile:
                birth_date = date.today() - timedelta(days=365*18)  # 18 anos atrás
                self.profile = StudentProfile.objects.create(
                    user=self.user,
                    full_name=self.user.full_name or self.user.username,
                    email=self.user.email,
                    phone=self.user.phone or '',
                    birth_date=birth_date,
                    cpf='00000000000',  # CPF mínimo obrigatório
                    rg='00000000',  # RG mínimo obrigatório
                    cep='00000000',  # CEP mínimo obrigatório
                    address='Não informado',
                    address_number='0',
                )
            
            self.profile.photo = self.cleaned_data['photo']
            self.profile.save()
        
        return self.user


class EmployeeEditForm(forms.ModelForm):
    """Formulário para edição de funcionário"""
    
    class Meta:
        model = EmployeeProfile
        fields = [
            'full_name', 'email', 'phone', 'birth_date',
            'cpf', 'rg', 'cep', 'address', 'address_number', 'address_complement',
            'photo', 'department', 'position'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'photo': forms.FileInput(),
            'department': forms.Select(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # CPF somente leitura
        self.fields['cpf'].widget.attrs['readonly'] = True
        self.fields['cpf'].widget.attrs['class'] = 'bg-gray-100 cursor-not-allowed'
        
        # Adiciona classes CSS
        for field_name, field in self.fields.items():
            if field.widget:
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'


class InstructorVehicleForm(forms.ModelForm):
    """Formulário para edição dos dados do veículo do instrutor"""

    class Meta:
        model = InstructorVehicle
        fields = [
            'plate', 'renavam', 'make', 'model', 'color', 'year',
            'dual_control', 'adapted_pcd'
        ]
        labels = {
            'plate': 'Placa',
            'renavam': 'RENAVAM',
            'make': 'Marca',
            'model': 'Modelo',
            'color': 'Cor',
            'year': 'Ano',
            'dual_control': 'Possui acionamento duplo (pedais no passageiro)',
            'adapted_pcd': 'Veículo adaptado para PCD',
        }
        widgets = {
            'plate': forms.TextInput(attrs={'placeholder': 'ABC1D23 ou AAA-1234'}),
            'renavam': forms.TextInput(attrs={'placeholder': '11 dígitos'}),
            'make': forms.TextInput(attrs={'placeholder': 'Ex.: Chevrolet'}),
            'model': forms.TextInput(attrs={'placeholder': 'Ex.: Onix 1.0'}),
            'color': forms.TextInput(attrs={'placeholder': 'Ex.: Prata'}),
            'year': forms.NumberInput(attrs={'min': 1960, 'placeholder': 'Ex.: 2022'}),
        }

    def clean_plate(self):
        plate = (self.cleaned_data.get('plate') or '').strip().upper()
        import re
        pattern_old = re.compile(r'^[A-Z]{3}-?\d{4}$')
        pattern_mercosul = re.compile(r'^[A-Z]{3}-?[0-9][A-Z][0-9]{2}$')
        if not (pattern_old.match(plate) or pattern_mercosul.match(plate)):
            raise ValidationError('Placa inválida. Use AAA-1234 ou ABC1D23.')
        return plate.replace('-', '')

    def clean_renavam(self):
        ren = ''.join(filter(str.isdigit, self.cleaned_data.get('renavam') or ''))
        if len(ren) != 11:
            raise ValidationError('RENAVAM deve conter exatamente 11 dígitos.')
        return ren

    def clean_year(self):
        from datetime import date
        year = self.cleaned_data.get('year')
        current_year = date.today().year
        if not year or year < 1960 or year > current_year + 1:
            raise ValidationError(f"Ano deve estar entre 1960 e {current_year + 1}.")
        return year