from django.contrib import admin

from registration_app.services_fabric.services_activity import Activity
from registration_app.services_fabric.services_course import Course
from registration_app.services_fabric.services_student import Student
from registration_app.services_fabric.services_student_activity_grade import StudentActivityGrade
from registration_app.services_fabric.services_student_course import StudentCourse
from registration_app.services_fabric.services_student_course_grade import StudentCourseGrade
from registration_app.services_fabric.services_title import Title

admin.site.register(Title)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Activity)
admin.site.register(StudentCourse)
admin.site.register(StudentActivityGrade)
admin.site.register(StudentCourseGrade)
