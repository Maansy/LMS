from rest_framework import permissions


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
        return request.user.enrollments.filter(course__id=view.kwargs['course_id']).exists()
