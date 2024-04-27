from django.urls import path
from lms_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.sign_up, name='register'),
    path('subject-selection/', views.subject_selection, name='subject_selection_url'),
    path('create-task/', views.create_task, name='create_task'),
    path('task-list/', views.task_list, name='task_list'),
    path('select-subject/', views.select_subject, name='select_subject'),
    path('record-attendance/<int:subject_id>/', views.record_attendance, name='record_attendance'),
    path('submit_task/<int:task_id>/', views.submit_task, name='submit_task'),
    path('submit_task/', views.submit_task, name='submit_task_default'),
]
