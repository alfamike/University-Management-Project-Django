from django import forms
from registration_app.models import Course, Title
from registration_app.services_fabric import services_title, services_course, services_student, services_activity, \
    services_student_activity_grade, services_student_course_grade


class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = ['name', 'description']
