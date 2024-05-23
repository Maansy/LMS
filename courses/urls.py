# courses/urls.py

from django.urls import path
from .views import (
    CourseListCreateView, CourseDetailView,
    ModuleListCreateView, ModuleDetailView,
    LessonListCreateView, LessonDetailView,
    EnrollmentListCreateView, LessonProgressUpdateView
)

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:course_id>/modules/', ModuleListCreateView.as_view(), name='module-list-create'),
    path('courses/<int:course_id>/modules/<int:pk>/', ModuleDetailView.as_view(), name='module-detail'),
    path('courses/<int:course_id>/modules/<int:module_id>/lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('courses/<int:course_id>/modules/<int:module_id>/lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('enrollments/', EnrollmentListCreateView.as_view(), name='enrollment-list-create'),
    path('lessons/<int:lesson_id>/progress/', LessonProgressUpdateView.as_view(), name='lesson-progress-update'),
]
