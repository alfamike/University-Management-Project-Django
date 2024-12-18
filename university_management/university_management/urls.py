"""
URL configuration for university_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from registration_app import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Home
    path('', views.home, name='home'),

    # Login
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Chat
    path('chat/', views.chat_view, name='chat'),

    # Student
    path('createStudent/', views.create_student, name='create_student'),
    path('students/', views.student_list, name='student_list'),

    # Course
    path('createCourse/', views.create_course, name='create_course'),
    path('courses/', views.course_list, name='course_list'),

    # Title
    path('createTitle/', views.create_title, name='create_title'),
    path('titles/', views.title_list, name='title_list'),
]
