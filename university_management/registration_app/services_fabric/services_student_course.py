import asyncio
import json
import os
import uuid

from django.db import models
from hfc.fabric import Client

from registration_app.services_fabric.services_course import Course
from registration_app.services_fabric.services_fabric import HyperledgeFabric
from registration_app.services_fabric.services_student import Student


class StudentCourse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, related_name='courses', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='students', on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_student_course_grade')
        ]

    def __str__(self):
        return f"{self.student} - {self.course}"

    def save(self, *args, **kwargs):

        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        existing_student_course = (
            StudentCourse.get_student_course_by_params(
                str(self.student.primary_key), str(self.course.primary_key)))

        if existing_student_course is not None:
            response = loop.run_until_complete(HyperledgeFabric.invoke_chaincode(
                'student_course_cc',
                'UpdateStudentCourse',
                [str(self.pk), str(self.student.primary_key), str(self.course.primary_key), self.grade,
                 self.is_deleted]
            ))
        else:
            response = loop.run_until_complete(HyperledgeFabric.invoke_chaincode(
                'student_course_cc',
                'CreateStudentCourse',
                [str(self.pk), str(self.student.primary_key), str(self.course.primary_key), self.grade,
                 self.is_deleted]
            ))

        return response

    def delete(self, *args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.invoke_chaincode(
            'student_course_cc',
            'UpdateStudentCourse',
            [str(self.pk), str(self.student.primary_key), str(self.course.primary_key), self.grade,
             'true']
        ))
        return response

    @classmethod
    def all(cls):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            'student_course_cc',
            'GetAllStudentCourses',
            []
        ))
        student_courses = json.loads(response)['student_courses']
        student_courses_res = []
        for student_course in student_courses:
            student_courses_res.append(cls(student=Student.get_student(student_course['student_id']),
                                           course=Course.get_course(student_course['course_id']),
                                           grade=student_course['grade']))
        return student_courses_res

    @classmethod
    def get_courses_by_student(cls, student_id):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            'student_course_cc',
            'GetCoursesByStudent',
            [student_id]
        ))
        courses = json.loads(response)['courses']
        courses_res = []
        for course in courses:
            courses_res.append(Course.get_course(course['course_id']))
        return courses_res

    @classmethod
    def get_students_by_course(cls, course_id):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            'student_course_cc',
            'GetStudentsByCourse',
            [course_id]
        ))
        students = json.loads(response)['students']
        students_res = []
        for student in students:
            students_res.append(Student.get_student(student['student_id']))
        return students_res

    @classmethod
    def get_student_course(cls, student_course_id):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            'student_course_cc',
            'QueryStudentCourse',
            [student_course_id]
        ))
        student_course = json.loads(response)
        student_course = cls(student=Student.get_student(student_course['student_id']),
                             course=Course.get_course(student_course['course_id']), grade=student_course['grade'])
        return student_course

    @classmethod
    def get_student_course_by_params(cls, student_id, course_id):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            'student_course_cc',
            'GetStudentCourseByParams',
            [student_id, course_id]
        ))
        return response
