from django.urls import path
from lms_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.sign_up, name='register'),
    path('subject-selection/', views.subject_selection, name='subject_selection_url'),
]