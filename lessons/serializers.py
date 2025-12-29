from rest_framework import serializers
from .models import Lesson
from accounts.models import InstructorVehicle


class InstructorVehicleSerializer(serializers.ModelSerializer):
    """Serializer para veículos do instrutor"""
    class Meta:
        model = InstructorVehicle
        fields = [
            'id', 'plate', 'renavam', 'make', 'model', 'color', 'year',
            'dual_control', 'adapted_pcd'
        ]


class LessonSerializer(serializers.ModelSerializer):
    """Serializer para aulas"""
    instructor_name = serializers.CharField(source='instructor.full_name', read_only=True)
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    vehicle_info = InstructorVehicleSerializer(source='vehicle', read_only=True)
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'student', 'student_name', 'instructor', 'instructor_name',
            'date', 'time', 'duration', 'location', 'vehicle_type', 'vehicle',
            'vehicle_info', 'status', 'prefer_dual_control', 'prefer_adapted_pcd',
            'score', 'notes', 'lesson_number', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'lesson_number']
