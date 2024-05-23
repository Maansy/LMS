from django.contrib import admin
from .models import Course, Module, Lesson

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'course__name']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'module__name']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'instructor', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'instructor__username']

admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)