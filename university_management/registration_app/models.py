from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)

    def __str__(self):
        return self.name
