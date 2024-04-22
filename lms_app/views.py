from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
from lms_app.forms import RegisterForm
from django.contrib.auth import login, logout
from lms_app.models import Student, Subject, Faculty


def index(request):
    return render(request, 'index.html')


class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('index')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


def logout_view(request):
    logout(request)
    return redirect('login')


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
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
        try:
            student = Student.objects.get(student_id=student_id)
            faculty = student.faculty
            subjects = Subject.objects.filter(faculties=faculty)
            registered_subjects = student.subjects.all().values_list('id', flat=True)
            available_subjects = subjects.exclude(id__in=registered_subjects)
            return render(request, 'subject_selection.html', {'subjects': available_subjects})
        except Student.DoesNotExist:
            pass

    if request.method == 'POST' and request.POST.get('subject') is not None:
        student_name = request.user.username
        student = Student.objects.get(first_name=student_name)
        subject_name = request.POST.get('subject')
        subject = Subject.objects.get(name=subject_name)
        student.subjects.add(subject)
        student.save()

    return render(request, 'subject_selection.html', {'subjects': None})


