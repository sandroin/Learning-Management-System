from django import forms
from lms_app.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']


class CheckRegisteredUserForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'execution_date']
