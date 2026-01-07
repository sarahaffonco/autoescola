from django import forms
from .models import Lesson
from accounts.models import InstructorVehicle
from django.core.exceptions import ValidationError


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            'instructor', 'date', 'time', 'cep', 'numero',
            'rua', 'bairro', 'cidade', 'estado',
            'vehicle_type', 'vehicle', 'prefer_dual_control', 'prefer_adapted_pcd'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'cep': forms.TextInput(attrs={
                'placeholder': '00000-000',
                'maxlength': '9',
                'readonly': False
            }),
            'numero': forms.TextInput(attrs={
                'placeholder': '123',
                'maxlength': '10'
            }),
            'rua': forms.TextInput(attrs={'readonly': True}),
            'bairro': forms.TextInput(attrs={'readonly': True}),
            'cidade': forms.TextInput(attrs={'readonly': True}),
            'estado': forms.TextInput(attrs={'readonly': True, 'maxlength': '2'}),
        }

    def __init__(self, *args, **kwargs):
        # Allow passing the current student to enforce conflict checks
        self.student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        # Configura o queryset de veículos disponíveis
        self.fields['vehicle'].queryset = InstructorVehicle.objects.select_related('instructor').all()
        self.fields['vehicle'].required = False
        # Define campos opcionais
        self.fields['instructor'].required = False
        self.fields['vehicle_type'].required = False
        # Rótulos amigáveis
        self.fields['prefer_dual_control'].label = 'Preferência por veículo com acionamento duplo'
        self.fields['prefer_adapted_pcd'].label = 'Preferência por veículo adaptado para PCD'
        # CEP e localização
        self.fields['cep'].required = True
        self.fields['numero'].required = True
        self.fields['rua'].required = False
        self.fields['bairro'].required = False
        self.fields['cidade'].required = False
        self.fields['estado'].required = False

    def clean(self):
        """Normaliza CEP e valida conflitos de agendamento."""
        cleaned_data = super().clean()
        cep = cleaned_data.get('cep', '') or ''

        cep_digits = ''.join(filter(str.isdigit, cep))
        if cep_digits:
            if len(cep_digits) != 8:
                raise ValidationError({'cep': 'Informe um CEP válido com 8 dígitos.'})
            cleaned_data['cep'] = f"{cep_digits[:5]}-{cep_digits[5:]}"

        # Validações de conflito de agenda
        lesson_date = cleaned_data.get('date')
        lesson_time = cleaned_data.get('time')
        instructor = cleaned_data.get('instructor')

        # Apenas valida se data e hora foram informadas
        if lesson_date and lesson_time:
            blocking_statuses = ['pending', 'scheduled', 'in-progress']

            # Conflito do aluno: não pode ter duas aulas no mesmo dia e horário
            if self.student is not None:
                student_conflict = Lesson.objects.filter(
                    student=self.student,
                    date=lesson_date,
                    time=lesson_time,
                    status__in=blocking_statuses
                )
                # Ignora a própria instância em edição
                if self.instance and self.instance.pk:
                    student_conflict = student_conflict.exclude(pk=self.instance.pk)

                if student_conflict.exists():
                    raise ValidationError({'time': 'Você já possui uma aula neste dia e horário.'})

            # Conflito do instrutor: não permitir dois alunos com o mesmo instrutor no mesmo horário
            if instructor is not None:
                instructor_conflict = Lesson.objects.filter(
                    instructor=instructor,
                    date=lesson_date,
                    time=lesson_time,
                    status__in=blocking_statuses
                )
                if self.instance and self.instance.pk:
                    instructor_conflict = instructor_conflict.exclude(pk=self.instance.pk)

                if instructor_conflict.exists():
                    raise ValidationError({'time': 'Instrutor indisponível neste dia e horário.'})

        return cleaned_data
