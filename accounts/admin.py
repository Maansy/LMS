from django.contrib import admin
from .models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'role', 'first_name', 'last_name')
    list_filter = ('role',)
    ordering = ('username',)

admin.site.register(User, UserAdmin)