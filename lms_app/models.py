from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from lms_app.forms import RegisterForm, CheckRegisteredUserForm, TaskForm
from django.contrib.auth import login, logout
from lms_app.models import Student, Lecturer, CustomUser, Subject, Faculty


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


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.lecturer = request.user

            if task.execution_date < timezone.now().date():
                form.add_error('execution_date', 'Execution date must be in the future.')
                return render(request, 'create_task.html', {'form': form})

            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})


def task_list(request):
    tasks = request.user.tasks.all()
    return render(request, 'task_list.html', {'tasks': tasks})
