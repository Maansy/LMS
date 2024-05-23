# accounts/management/commands/create_groups.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import User


class Command(BaseCommand):
    help = 'Create default groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Create Instructor group
        instructor_group, created = Group.objects.get_or_create(name='Instructor')
        if created:
            self.stdout.write(self.style.SUCCESS('Instructor group created'))

        # Create Student group
        student_group, created = Group.objects.get_or_create(name='Student')
        if created:
            self.stdout.write(self.style.SUCCESS('Student group created'))

        # Add permissions to Instructor group
        content_type = ContentType.objects.get_for_model(User)
        instructor_permissions = Permission.objects.filter(content_type=content_type, codename__in=[
            'add_course', 'change_course', 'delete_course',
            'add_module', 'change_module', 'delete_module',
            'add_lesson', 'change_lesson', 'delete_lesson',
        ])
        instructor_group.permissions.set(instructor_permissions)

        # Add permissions to Student group
        student_permissions = Permission.objects.filter(content_type=content_type, codename__in=[
            'view_course', 'view_module', 'view_lesson',
        ])
        student_group.permissions.set(student_permissions)

        self.stdout.write(self.style.SUCCESS('Groups and permissions assigned successfully'))
