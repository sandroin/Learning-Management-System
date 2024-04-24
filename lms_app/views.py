from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from lms_app.forms import RegisterForm, CheckRegisteredUserForm
from django.contrib.auth import login, logout
from lms_app.models import Student, Lecturer, CustomUser


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
