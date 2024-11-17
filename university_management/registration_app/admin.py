from django.contrib import admin
from .models import Title, Course, Student, Activity, StudentActivityGrade

admin.site.register(Title)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Activity)
admin.site.register(StudentActivityGrade)
