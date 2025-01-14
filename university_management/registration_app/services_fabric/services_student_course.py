import json
import os
import uuid

from django.db import models
from hfc.fabric import Client

from registration_app.services_fabric.services_course import Course
from registration_app.services_fabric.services_fabric import query_chaincode, invoke_chaincode
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

        connection_profile_path = os.path.join(
            os.path.dirname(__file__),
            'connection-profile.json'
        )
        client = Client(net_profile=connection_profile_path)

        try:
            user = client.get_user(org_name='Org1', name='Admin')
            print("Fabric user retrieved successfully.")
        except ValueError as e:
            print(f"Error retrieving Fabric user: {e}")
            raise

        existing_student_course = (
            StudentCourse.get_student_course_by_params(
                str(self.student.primary_key), str(self.course.primary_key)))

        if existing_student_course is not None:
            response = invoke_chaincode(
                client,
                user,
                'student_course_cc',
                'UpdateStudentCourse',
                [str(self.pk), str(self.student.primary_key), str(self.course.primary_key), self.grade,
                 self.is_deleted]
            )
        else:
            response = invoke_chaincode(
                client,
                user,
                'student_course_cc',
                'CreateStudentCourse',
                [str(self.pk), str(self.student.primary_key), str(self.course.primary_key), self.grade,
                 self.is_deleted]
            )

        return response

    def delete(self, *args, **kwargs):
        connection_profile_path = os.path.join(
            os.path.dirname(__file__),
            'connection-profile.json'
        )
        client = Client(net_profile=connection_profile_path)

        try:
            user = client.get_user(org_name='Org1', name='Admin')
            print("Fabric user retrieved successfully.")
        except ValueError as e:
            print(f"Error retrieving Fabric user: {e}")
            raise

        response = invoke_chaincode(
            client,
            user,
            'student_course_cc',
            'UpdateStudentCourse',
            [str(self.pk), str(self.student.primary_key), str(self.course.primary_key), self.grade,
             'true']
        )
        return response

    @classmethod
    def all(cls):
        print("Entering save method of Title...")
        connection_profile_path = os.path.join(
            os.path.dirname(__file__),
            'connection-profile.json'
        )
        client = Client(net_profile=connection_profile_path)

        try:
            user = client.get_user(org_name='Org1', name='Admin')
            print("Fabric user retrieved successfully.")
        except ValueError as e:
            print(f"Error retrieving Fabric user: {e}")
            raise

        response = query_chaincode(
            client,
            user,
            'student_course_cc',
            'GetAllStudentCourses',
            []
        )
        student_courses = json.loads(response)['student_courses']
        student_courses_res = []
        for student_course in student_courses:
            student_courses_res.append(cls(student=Student.get_student(student_course['student_id']),
                                           course=Course.get_course(student_course['course_id']),
                                           grade=student_course['grade']))
        return student_courses_res

    @classmethod
    def get_courses_by_student(cls, student_id):
        connection_profile_path = os.path.join(
            os.path.dirname(__file__),
            'connection-profile.json'
        )
        client = Client(net_profile=connection_profile_path)

        try:
            user = client.get_user(org_name='Org1', name='Admin')
            print("Fabric user retrieved successfully.")
        except ValueError as e:
            print(f"Error retrieving Fabric user: {e}")
            raise
        response = query_chaincode(
            client,
            user,
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
        connection_profile_path = os.path.join(
            os.path.dirname(__file__),
            'connection-profile.json'
        )
        client = Client(net_profile=connection_profile_path)

        try:
            user = client.get_user(org_name='Org1', name='Admin')
            print("Fabric user retrieved successfully.")
        except ValueError as e:
            print(f"Error retrieving Fabric user: {e}")
            raise

        response = query_chaincode(
            client,
            user,
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
        connection_profile_path = os.path.join(
            os.path.dirname(__file__),
            'connection-profile.json'
        )
        client = Client(net_profile=connection_profile_path)

        try:
            user = client.get_user(org_name='Org1', name='Admin')
            print("Fabric user retrieved successfully.")
        except ValueError as e:
            print(f"Error retrieving Fabric user: {e}")
            raise

        response = query_chaincode(
            client,
            user,
            'student_course_cc',
            'QueryStudentCourse',
            [student_course_id]
        )
        student_course = json.loads(response)
        student_course = cls(student=Student.get_student(student_course['student_id']),
                             course=Course.get_course(student_course['course_id']), grade=student_course['grade'])
        return student_course

    @classmethod
    def get_student_course_by_params(cls, student_id, course_id):
        connection_profile_path = os.path.join(
            os.path.dirname(__file__),
            'connection-profile.json'
        )
        client = Client(net_profile=connection_profile_path)

        try:
            user = client.get_user(org_name='Org1', name='Admin')
            print("Fabric user retrieved successfully.")
        except ValueError as e:
            print(f"Error retrieving Fabric user: {e}")
            raise

        response = query_chaincode(
            client,
            user,
            'student_course_cc',
            'GetStudentCourseByParams',
            [student_id, course_id]
        )
        return response
