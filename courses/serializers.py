from rest_framework import serializers
from .models import Course, Module, Lesson, Enrollment, LessonProgress

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video', 'pdf', 'text_content', 'content_type', 'created_at', 'updated_at']

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


class EnrollmentSerializer(serializers.ModelSerializer):
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), source='course', write_only=True)
    course = serializers.ReadOnlyField(source='course.name')  # Read-only field to show the course name

    class Meta:
        model = Enrollment
        fields = ['id', 'course_id', 'course', 'enrolled_at']

    def create(self, validated_data):
        # Extract course from the validated data
        course = validated_data.pop('course')
        student = self.context['request'].user

        # Ensure the student is not already enrolled in the course
        if Enrollment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("You are already enrolled in this course.")

        # Create the enrollment
        enrollment = Enrollment.objects.create(student=student, course=course)
        return enrollment

class LessonProgressSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    lesson_id = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all(), source='lesson', write_only=True)

    class Meta:
        model = LessonProgress
        fields = ['id', 'lesson', 'lesson_id', 'completed', 'completed_at']
