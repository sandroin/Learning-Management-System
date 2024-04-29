from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from custom_user.models import CustomUser


class Faculty(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Faculty")
        verbose_name_plural = _("Faculties")


class Subject(models.Model):
    faculties = models.ManyToManyField(Faculty, related_name='subjects', verbose_name=_("Faculties"))
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    files = models.FileField(verbose_name=_("Files"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")
        ordering = ['name']


class Student(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_("Student"),
        related_name="student"
    )
    student_id = models.AutoField(primary_key=True, verbose_name=_("Student ID"))
    faculty = models.ForeignKey(Faculty, on_delete=models.RESTRICT, verbose_name=_("Faculty"))
    subjects = models.ManyToManyField(Subject, related_name='students', verbose_name=_("Subjects"))
    first_name = models.CharField(max_length=50, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=50, verbose_name=_("Last Name"))
    dob = models.DateField(verbose_name=_("Date of Birth"), blank=False)
    email = models.EmailField(verbose_name=_("Email"), blank=False)
    password = models.CharField(max_length=50, verbose_name=_("Password"))

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")
        ordering = ['student_id']


class Lecturer(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_("Lecturer"),
        related_name="lecturer"
    )
    subjects = models.ManyToManyField(Subject, related_name='lecturers', verbose_name=_("Subjects"))
    first_name = models.CharField(max_length=50, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=50, verbose_name=_("Last Name"))
    password = models.CharField(max_length=50, verbose_name=_("Password"))

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = _("Lecturer")
        verbose_name_plural = _("Lecturers")
        ordering = ['id']


class AttendanceRecord(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, verbose_name=_('Lecturer'))
    students = models.ManyToManyField(Student, related_name='attendance_records', verbose_name=_("Students"))
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_('Subject'))
    date = models.DateField(verbose_name=_("Date"))

    def __str__(self):
        return "Attendance of " + str(self.subject) + " on " + str(self.date)

    class Meta:
        verbose_name = "Attendance Record"
        verbose_name_plural = "Attendance Records"
        ordering = ['date']


class Task(models.Model):
    lecturer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    execution_date = models.DateField()
    submission_file = models.FileField(upload_to='task_submissions/', null=True, blank=True)
    submission_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['execution_date']
