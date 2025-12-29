from django import forms
from .models import Lesson
from accounts.models import InstructorVehicle


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
        super().__init__(*args, **kwargs)
        # Configura o queryset de veículos disponíveis
        self.fields['vehicle'].queryset = InstructorVehicle.objects.select_related('instructor').all()
        self.fields['vehicle'].required = False
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
