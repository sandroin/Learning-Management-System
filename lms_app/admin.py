from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from lms_app.models import Faculty, Subject, Student, Lecturer, CustomUser
from django.utils.translation import gettext_lazy as _


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'files')
    list_filter = ('name', 'faculties')
    search_fields = ('name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'dob', 'email', 'faculty')
    list_filter = ('faculty', 'subjects')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')
    list_filter = ('subjects',)
    search_fields = ('first_name', 'last_name')


@admin.register(CustomUser)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'status', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'status'),
        }),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    ordering = ['email']
