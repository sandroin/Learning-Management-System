from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


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
    files = models.FileField(verbose_name=_("Files"))
    faculties = models.ManyToManyField(Faculty, related_name='subjects', verbose_name=_("Faculties"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")
        ordering = ['name']


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        validate_email(email)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        # extra_fields.setdefault('is_active', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('status', 1)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('Email Address'), unique=True)

    class Status(IntegerChoices):
        lecturer = 1, _("Lecturer")
        student = 2, _("Student")

    status = models.PositiveSmallIntegerField(choices=Status.choices)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    # def save(self, *args, **kwargs):
    #     # Set is_active to False if it's not provided explicitly
    #     if self._state.adding and kwargs.get('is_superuser') is False and 'is_active' not in kwargs:
    #         self.is_active = False
    #
    #     super().save(*args, **kwargs)


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
    dob = models.DateField(verbose_name=_("Date of Birth"))
    email = models.EmailField(verbose_name=_("Email"))
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
    id = models.AutoField(primary_key=True, verbose_name=_("ID"))
    first_name = models.CharField(max_length=50, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=50, verbose_name=_("Last Name"))
    subjects = models.ManyToManyField(Subject, related_name='lecturers', verbose_name=_("Subjects"))
    password = models.CharField(max_length=50, verbose_name=_("Password"))

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = _("Lecturer")
        verbose_name_plural = _("Lecturers")
        ordering = ['id']
