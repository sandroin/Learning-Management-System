from django.contrib import admin
from lms_app.models import Faculty, Subject, Student, Lecturer


class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(Faculty, FacultyAdmin)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'files')
    list_filter = ('name', 'faculties')
    search_fields = ('name',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'files':
            kwargs['widget'].attrs['maxlength'] = 1024 * 1024 * 10 
        return super().formfield_for_dbfield(db_field, **kwargs)




admin.site.register(Subject, SubjectAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'dob', 'email', 'faculty')
    list_filter = ('faculty', 'subjects')
    search_fields = ('first_name', 'last_name', 'email')


admin.site.register(Student, StudentAdmin)


class LecturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')
    list_filter = ('subjects',)
    search_fields = ('first_name', 'last_name')


admin.site.register(Lecturer, LecturerAdmin)
