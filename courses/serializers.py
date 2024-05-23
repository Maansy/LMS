# courses/serializers.py

from rest_framework import serializers
from .models import Course, Module, Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video', 'pdf', 'text_content', 'content_type', 'created_at', 'updated_at']
        extra_kwargs = {
            'video': {'required': False},
            'pdf': {'required': False},
            'text_content': {'required': False},
            'content_type': {'required': False},
        }

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'name', 'description', 'lessons', 'created_at', 'updated_at']

class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    instructor = serializers.ReadOnlyField(source='instructor.username')

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'instructor', 'modules', 'created_at', 'updated_at']
