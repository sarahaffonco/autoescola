from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, time, timedelta
from accounts.models import User
from lessons.models import Lesson, StudentProgress


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo'

    def handle(self, *args, **kwargs):
        self.stdout.write('Criando usuários...')
        
        # Create instructor
        instrutor, created = User.objects.get_or_create(
            username='carlos_mendes',
            defaults={
                'email': 'carlos@autoescola.com',
                'full_name': 'Carlos Mendes',
                'phone': '(11) 98765-4321',
                'role': 'instrutor',
            }
        )
        if created:
            instrutor.set_password('senha123')
            instrutor.save()
            self.stdout.write(self.style.SUCCESS(f'Instrutor criado: {instrutor.full_name}'))
        
        # Create students
        students_data = [
            {
                'username': 'maria_silva',
                'email': 'maria@email.com',
                'full_name': 'Maria Silva',
                'phone': '(11) 91234-5678',
            },
            {
                'username': 'joao_santos',
                'email': 'joao@email.com',
                'full_name': 'João Santos',
                'phone': '(11) 92345-6789',
            },
            {
                'username': 'ana_costa',
                'email': 'ana@email.com',
                'full_name': 'Ana Costa',
                'phone': '(11) 93456-7890',
            },
        ]
        
        students = []
        for student_data in students_data:
            student, created = User.objects.get_or_create(
                username=student_data['username'],
                defaults={
                    'email': student_data['email'],
                    'full_name': student_data['full_name'],
                    'phone': student_data['phone'],
                    'role': 'aluno',
                }
            )
            if created:
                student.set_password('senha123')
                student.save()
                self.stdout.write(self.style.SUCCESS(f'Aluno criado: {student.full_name}'))
            students.append(student)
        
        self.stdout.write('Criando aulas...')
        
        # Create lessons
        today = date.today()
        lessons_data = [
            {
                'student': students[0],
                'date': today,
                'time': time(8, 0),
                'location': 'Centro - Av. Principal, 123',
                'vehicle_type': 'B',
                'status': 'scheduled',
                'lesson_number': 12,
            },
            {
                'student': students[1],
                'date': today,
                'time': time(9, 0),
                'location': 'Zona Sul - Rua das Flores, 456',
                'vehicle_type': 'B',
                'status': 'in-progress',
                'lesson_number': 8,
            },
            {
                'student': students[2],
                'date': today,
                'time': time(10, 0),
                'location': 'Centro - Av. Principal, 123',
                'vehicle_type': 'A',
                'status': 'scheduled',
                'lesson_number': 15,
            },
            {
                'student': students[0],
                'date': today - timedelta(days=1),
                'time': time(14, 0),
                'location': 'Zona Norte - Av. Brasil, 789',
                'vehicle_type': 'B',
                'status': 'completed',
                'lesson_number': 11,
                'score': 'Excelente',
            },
        ]
        
        for lesson_data in lessons_data:
            lesson, created = Lesson.objects.get_or_create(
                instructor=instrutor,
                student=lesson_data['student'],
                date=lesson_data['date'],
                time=lesson_data['time'],
                defaults={
                    'location': lesson_data['location'],
                    'vehicle_type': lesson_data['vehicle_type'],
                    'status': lesson_data['status'],
                    'lesson_number': lesson_data['lesson_number'],
                    'score': lesson_data.get('score', ''),
                    'duration': 50,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Aula criada: {lesson.student.full_name} - {lesson.date}'))
        
        # Create student progress
        self.stdout.write('Criando progresso dos alunos...')
        
        skills = ['baliza', 'estacionamento', 'direcao_via', 'conversoes', 'ladeira']
        for student in students:
            for skill in skills:
                progress_value = 60 + (hash(f"{student.id}{skill}") % 40)  # Random value between 60-100
                progress, created = StudentProgress.objects.get_or_create(
                    student=student,
                    skill=skill,
                    defaults={'progress': progress_value}
                )
                if created:
                    self.stdout.write(f'  {student.full_name} - {skill}: {progress_value}%')
        
        self.stdout.write(self.style.SUCCESS('\nDados de exemplo criados com sucesso!'))
        self.stdout.write('\nCredenciais de teste:')
        self.stdout.write('  Instrutor: carlos_mendes / senha123')
        self.stdout.write('  Aluno: maria_silva / senha123')
        self.stdout.write('  Aluno: joao_santos / senha123')
        self.stdout.write('  Aluno: ana_costa / senha123')
