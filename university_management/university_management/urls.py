from django.urls import path
from registration_app import views, auth

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Login
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # Auth
    path('get_nonce/', auth.get_nonce, name='nonce'),
    path('verify_signature/', auth.verify_signature, name='verify_signature'),

    # Chat
    path('chat/', views.chat_view, name='chat'),

    # Student
    path('createStudent/', views.create_student, name='create_student'),
    path('modifyStudent/', views.modify_student, name='modify_student'),
    path('removeStudent/', views.remove_student, name='remove_student'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:pk>/', views.student_record, name='student_record'),
    path('deEnrollCourses/', views.de_enroll_courses, name='de_enroll_student'),
    path('enrollCourses/', views.enroll_courses, name='enroll_student'),

    # Course
    path('createCourse/', views.create_course, name='create_course'),
    path('modifyCourse/', views.modify_course, name='modify_course'),
    path('removeCourse/', views.remove_course, name='modify_course'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_record, name='course_record'),
    path('manageGradeToCourse/', views.manage_grade_to_course, name='manage_grade_to_course'),

    # Title
    path('createTitle/', views.create_title, name='create_title'),
    path('modifyTitle/', views.modify_title, name='modify_title'),
    path('removeTitle/', views.remove_title, name='remove_title'),
    path('titles/', views.title_list, name='title_list'),
    path('titles/<int:pk>/', views.title_record, name='title_record'),

    # Activity
    path('createActivity/', views.create_activity, name='create_activity'),
    path('removeActivity/', views.remove_activity, name='remove_activity'),
    path('modifyActivity/', views.modify_activity, name='modify_activity'),
    path('get_activities_by_course_of_activity_grades/', views.get_activities_by_course_of_activity_grades,
         name='get_activities_by_course_of_activity_grades'),
    path('manageGradeToActivity/', views.manage_grade_to_activity, name='manage_grade_to_activity'),
]
