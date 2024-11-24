from django import forms
from registration_app.models import Student, Course, Title
from registration_app.services_fabric import services_title, services_course, services_student, services_activity, \
    services_student_activity_grade, services_student_course_grade


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email']
