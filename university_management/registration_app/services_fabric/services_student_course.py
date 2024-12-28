from registration_app.services_fabric.services_course import Course
from registration_app.services_fabric.services_fabric import get_fabric_client
from registration_app.services_fabric.services_fabric import get_fabric_client
from django.db.models import QuerySet
from django.apps import apps
from registration_app.services_fabric.services_fabric import get_fabric_client
import json
import uuid
from django.db import models
from registration_app.services_fabric import services_title, services_course, services_student, services_activity, \
    services_student_activity_grade, services_student_course_grade
from registration_app.services_fabric.services_fabric import query_chaincode, get_fabric_client, invoke_chaincode
from registration_app.services_fabric.services_student import Student
from registration_app.services_fabric.services_title import Title


class StudentCourse(models.Model):
    student = models.ForeignKey(Student, related_name='courses', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='students', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_student_course')
        ]

    def __str__(self):
        return f"{self.student} - {self.course}"

    def save(self, *args, **kwargs):

        client = get_fabric_client()

        existing_student_course = StudentCourse.get_student_course(str(self.pk))

        if existing_student_course is not None:
            response = invoke_chaincode(
                client,
                'student_course_cc',
                'UpdateStudentCourse',
                [str(self.pk), str(self.student.primary_key), str(self.course.primary_key)]
            )
        else:
            response = invoke_chaincode(
                client,
                'student_course_cc',
                'CreateStudentCourse',
                [str(self.pk), str(self.student.primary_key), str(self.course.primary_key)]
            )

        return response

    def delete(self, *args, **kwargs):

        client = get_fabric_client()

        response = invoke_chaincode(
            client,
            'student_course_cc',
            'UpdateStudentCourse',
            [str(self.pk), str(self.student.primary_key), str(self.course.primary_key), 'true']
        )
        return response

    @classmethod
    def all(cls):
        client = get_fabric_client()

        response = query_chaincode(
            client,
            'student_course_cc',
            'GetAllStudentCourses',
            []
        )
        student_courses = json.loads(response)['student_courses']
        student_courses_res = []
        for student_course in student_courses:
            student_courses_res.append(cls(student=Student.get_student(student_course['student_id']),
                                           course=Course.get_course(student_course['course_id'])))
        return student_courses_res

    @classmethod
    def get_courses_by_student(cls, student_id):
        client = get_fabric_client()
        response = query_chaincode(
            client,
            'student_course_cc',
            'GetCoursesByStudent',
            [student_id]
        )
        courses = json.loads(response)['courses']
        courses_res = []
        for course in courses:
            courses_res.append(Course.get_course(course['course_id']))
        return courses_res

    @classmethod
    def get_students_by_course(cls, course_id):
        client = get_fabric_client()
        response = query_chaincode(
            client,
            'student_course_cc',
            'GetStudentsByCourse',
            [course_id]
        )
        students = json.loads(response)['students']
        students_res = []
        for student in students:
            students_res.append(Student.get_student(student['student_id']))
        return students_res

    @classmethod
    def get_student_course(cls, student_course_id):
        client = get_fabric_client()
        response = query_chaincode(
            client,
            'student_course_cc',
            'QueryStudentCourse',
            [student_course_id]
        )
        student_course = json.loads(response)
        student_course = cls(student=Student.get_student(student_course['student_id']),
                             course=Course.get_course(student_course['course_id']))
        return student_course
