from django import forms
from .models import Lesson
from accounts.models import InstructorVehicle


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            'instructor', 'date', 'time', 'location', 'vehicle_type',
            'vehicle', 'prefer_dual_control', 'prefer_adapted_pcd'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configura o queryset de veículos disponíveis
        self.fields['vehicle'].queryset = InstructorVehicle.objects.select_related('instructor').all()
        self.fields['vehicle'].required = False
        # Rótulos amigáveis
        self.fields['prefer_dual_control'].label = 'Preferência por veículo com acionamento duplo'
        self.fields['prefer_adapted_pcd'].label = 'Preferência por veículo adaptado para PCD'
