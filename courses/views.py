from rest_framework import generics, permissions, status, parsers
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Course, Module, Lesson, Enrollment, LessonProgress
from .serializers import CourseSerializer, ModuleSerializer, LessonSerializer, EnrollmentSerializer, LessonProgressSerializer

class IsInstructorOfCourse(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.instructor == request.user

class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'instructor'

class IsEnrolledInCourse(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'instructor':
            return False
        return Enrollment.objects.filter(student=request.user, course__id=view.kwargs['course_id']).exists()

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.role != 'instructor':
            raise PermissionDenied("Only instructors can create courses.")
        serializer.save(instructor=self.request.user)

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsInstructorOfCourse]


class ModuleListCreateView(generics.ListCreateAPIView):
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Module.objects.filter(course__id=self.kwargs['course_id'])

    def perform_create(self, serializer):
        course = Course.objects.get(id=self.kwargs['course_id'])
        if course.instructor != self.request.user:
            raise PermissionDenied("You do not have permission to add modules to this course.")
        serializer.save(course=course)

class ModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        module = super().get_object()
        if module.course.instructor != self.request.user:
            raise PermissionDenied("You do not have permission to modify this module.")
        return module


class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_queryset(self):
        return Lesson.objects.filter(module__id=self.kwargs['module_id'], module__course__id=self.kwargs['course_id'])

    def perform_create(self, serializer):
        module = Module.objects.get(id=self.kwargs['module_id'], course__id=self.kwargs['course_id'])
        if module.course.instructor != self.request.user:
            raise PermissionDenied("You do not have permission to add lessons to this module.")
        serializer.save(module=module)

class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        lesson = super().get_object()
        if lesson.module.course.instructor != self.request.user:
            if self.request.user.role == 'student':
                enrollment = Enrollment.objects.filter(student=self.request.user, course=lesson.module.course).exists()
                if not enrollment:
                    raise PermissionDenied("You must be enrolled in the course to view this lesson.")
            else:
                raise PermissionDenied("You do not have permission to modify this lesson.")
        return lesson


class EnrollmentListCreateView(generics.ListCreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.role == 'instructor':
            raise PermissionDenied("Instructors cannot enroll in courses.")
        serializer.save()

class LessonProgressUpdateView(generics.UpdateAPIView):
    serializer_class = LessonProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LessonProgress.objects.filter(enrollment__student=self.request.user, lesson__id=self.kwargs['lesson_id'])

    def perform_update(self, serializer):
        serializer.save(completed=True, completed_at=timezone.now())
