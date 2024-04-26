from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from lms_app.forms import RegisterForm, CheckRegisteredUserForm
from django.contrib.auth import login, logout
from lms_app.models import Student, Lecturer, CustomUser, Subject, Faculty, AttendanceRecord


def index(request):
    return render(request, 'index.html')


class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('index')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password')
        return self.render_to_response(self.get_context_data(form=form))


def logout_view(request):
    logout(request)
    return redirect('login')


def sign_up(request):
    form = RegisterForm()
    if request.method == 'GET':
        return render(request, 'registration/register.html', {'form': form})

    if request.method == 'POST':
        user = get_object_or_404(CustomUser, email=request.POST.get('email'))
        form = CheckRegisteredUserForm(request.POST, instance=user)
        if form.is_valid():
            user.is_active = True
            user = form.save(commit=False)
            user.save()

            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('login')
        else:
            return render(request, 'registration/register.html', {'form': form})


def subject_selection(request):
    # temporary part, needs to be developed!
    if request.method == 'POST' and request.POST.get('subject') is None:
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, student_id=student_id)
        faculty = student.faculty
        subjects = Subject.objects.filter(faculties=faculty)
        registered_subjects = student.subjects.all().values_list('id', flat=True)
        available_subjects = subjects.exclude(id__in=registered_subjects)

        return render(request, 'subject_selection.html', {'subjects': available_subjects})

    if request.method == 'POST' and request.POST.get('subject') is not None:
        student_name = request.user.username
        student = Student.objects.get(first_name=student_name)
        subject_name = request.POST.get('subject')
        subject = Subject.objects.get(name=subject_name)
        student.subjects.add(subject)
        student.save()

    return render(request, 'subject_selection.html', {'subjects': None})


def select_subject(request):
    subjects = Subject.objects.all()
    return render(request, 'select_subject.html', {'subjects': subjects})


def record_attendance(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    students = subject.students.all()
    if request.method == 'POST':
        selected_student_emails = request.POST.getlist('selected_students')
        selected_students = Student.objects.filter(email__in=selected_student_emails)
        date = request.POST.get('date')
        lecturer = Lecturer.objects.get(user=request.user)
        attendance_record = AttendanceRecord.objects.create(
            subject=subject,
            date=date,
            lecturer=lecturer
        )
        attendance_record.students.set(selected_students)
        return redirect('index')
    return render(request, 'attendance.html', {'subject': subject, 'students': students})


