from django.urls import path

from registration_app import auth
from registration_app.views import general_views, student_views, course_views, title_views, activity_views

urlpatterns = [
    # Front
    path('', general_views.login, name='login'),  # URL pattern for the login view

    # Home
    path('home/', general_views.home, name='home'),  # URL pattern for the home view

    # Login
    path('logout/', general_views.logout, name='logout'),  # URL pattern for the logout view

    # Auth
    path('get_nonce/', auth.get_nonce, name='nonce'),  # URL pattern for getting a nonce
    path('verify_signature/', auth.verify_signature, name='verify_signature'),  # URL pattern for verifying a signature

    # Chat
    path('chat/', general_views.chat_view, name='chat'),  # URL pattern for the chat view

    # Student
    path('createStudent/', student_views.create_student, name='create_student'),  # URL pattern for creating a student
    path('modifyStudent/', student_views.modify_student, name='modify_student'),  # URL pattern for modifying a student
    path('removeStudent/', student_views.remove_student, name='remove_student'),  # URL pattern for removing a student
    path('students/', student_views.student_list, name='student_list'),  # URL pattern for listing students
    path('students/<int:pk>/', student_views.student_record, name='student_record'),  # URL pattern for a student's record
    path('deEnrollCourses/', student_views.de_enroll_courses, name='de_enroll_student'),  # URL pattern for de-enrolling courses
    path('enrollCourses/', student_views.enroll_courses, name='enroll_student'),  # URL pattern for enrolling courses

    # Course
    path('createCourse/', course_views.create_course, name='create_course'),  # URL pattern for creating a course
    path('modifyCourse/', course_views.modify_course, name='modify_course'),  # URL pattern for modifying a course
    path('removeCourse/', course_views.remove_course, name='modify_course'),  # URL pattern for removing a course
    path('courses/', course_views.course_list, name='course_list'),  # URL pattern for listing courses
    path('courses/<int:pk>/', course_views.course_record, name='course_record'),  # URL pattern for a course's record
    path('manageGradeToCourse/', course_views.manage_grade_to_course, name='manage_grade_to_course'),  # URL pattern for managing grades to a course

    # Title
    path('createTitle/', title_views.create_title, name='create_title'),  # URL pattern for creating a title
    path('modifyTitle/', title_views.modify_title, name='modify_title'),  # URL pattern for modifying a title
    path('removeTitle/', title_views.remove_title, name='remove_title'),  # URL pattern for removing a title
    path('titles/', title_views.title_list, name='title_list'),  # URL pattern for listing titles
    path('titles/<int:pk>/', title_views.title_record, name='title_record'),  # URL pattern for a title's record

    # Activity
    path('createActivity/', activity_views.create_activity, name='create_activity'),  # URL pattern for creating an activity
    path('removeActivity/', activity_views.remove_activity, name='remove_activity'),  # URL pattern for removing an activity
    path('modifyActivity/', activity_views.modify_activity, name='modify_activity'),  # URL pattern for modifying an activity
    path('get_activities_by_course_of_activity_grades/', student_views.get_activities_by_course_of_activity_grades,
         name='get_activities_by_course_of_activity_grades'),  # URL pattern for getting activities by course of activity grades
    path('manageGradeToActivity/', activity_views.manage_grade_to_activity, name='manage_grade_to_activity'),  # URL pattern for managing grades to an activity
]