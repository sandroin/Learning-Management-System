from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileSizeValidator

class Faculty(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Faculty")
        verbose_name_plural = _("Faculties")


class Subject(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    files = models.FileField(verbose_name=_("Files"), validators=[FileSizeValidator(max_size=5 * 1024 * 1024)])
    faculties = models.ManyToManyField(Faculty, related_name='subjects', verbose_name=_("Faculties"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")
        ordering = ['name']


class Student(models.Model):
    student_id = models.AutoField(primary_key=True, verbose_name=_("Student ID"))
    faculty = models.ForeignKey(Faculty, on_delete=models.RESTRICT, verbose_name=_("Faculty"))
    subjects = models.ManyToManyField(Subject, related_name='students', verbose_name=_("Subjects"))
    first_name = models.CharField(max_length=50, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=50, verbose_name=_("Last Name"))
    dob = models.DateField(verbose_name=_("Date of Birth"), blank=False)
    email = models.EmailField(verbose_name=_("Email"), blank=False)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")
        ordering = ['student_id']


class Lecturer(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_("ID"))
    first_name = models.CharField(max_length=50, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=50, verbose_name=_("Last Name"))
    subjects = models.ManyToManyField(Subject, related_name='lecturers', verbose_name=_("Subjects"))

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = _("Lecturer")
        verbose_name_plural = _("Lecturers")
        ordering = ['id']