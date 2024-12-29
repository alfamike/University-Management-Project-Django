from django.urls import path

from registration_app import auth
from registration_app.views import general_views, student_views, course_views, title_views, activity_views

urlpatterns = [
    # Home
    path('', general_views.home, name='home'),

    # Login
    path('login/', general_views.login, name='login'),
    path('logout/', general_views.logout, name='logout'),

    # Auth
    path('get_nonce/', auth.get_nonce, name='nonce'),
    path('verify_signature/', auth.verify_signature, name='verify_signature'),

    # Chat
    path('chat/', general_views.chat_view, name='chat'),

    # Student
    path('createStudent/', student_views.create_student, name='create_student'),
    path('modifyStudent/', student_views.modify_student, name='modify_student'),
    path('removeStudent/', student_views.remove_student, name='remove_student'),
    path('students/', student_views.student_list, name='student_list'),
    path('students/<int:pk>/', student_views.student_record, name='student_record'),
    path('deEnrollCourses/', student_views.de_enroll_courses, name='de_enroll_student'),
    path('enrollCourses/', student_views.enroll_courses, name='enroll_student'),

    # Course
    path('createCourse/', course_views.create_course, name='create_course'),
    path('modifyCourse/', course_views.modify_course, name='modify_course'),
    path('removeCourse/', course_views.remove_course, name='modify_course'),
    path('courses/', course_views.course_list, name='course_list'),
    path('courses/<int:pk>/', course_views.course_record, name='course_record'),
    path('manageGradeToCourse/', course_views.manage_grade_to_course, name='manage_grade_to_course'),

    # Title
    path('createTitle/', title_views.create_title, name='create_title'),
    path('modifyTitle/', title_views.modify_title, name='modify_title'),
    path('removeTitle/', title_views.remove_title, name='remove_title'),
    path('titles/', title_views.title_list, name='title_list'),
    path('titles/<int:pk>/', title_views.title_record, name='title_record'),

    # Activity
    path('createActivity/', activity_views.create_activity, name='create_activity'),
    path('removeActivity/', activity_views.remove_activity, name='remove_activity'),
    path('modifyActivity/', activity_views.modify_activity, name='modify_activity'),
    path('get_activities_by_course_of_activity_grades/', student_views.get_activities_by_course_of_activity_grades,
         name='get_activities_by_course_of_activity_grades'),
    path('manageGradeToActivity/', activity_views.manage_grade_to_activity, name='manage_grade_to_activity'),
]
