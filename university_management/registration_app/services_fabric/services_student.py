import json
import os
import uuid

from django.db import models
from hfc.fabric import Client

from registration_app.services_fabric.services_fabric import query_chaincode, invoke_chaincode


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

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
        existing_student = Student.get_student(str(self.pk))

        if existing_student is not None:
            response = invoke_chaincode(
                client,
                user,
                'student_cc',
                'UpdateStudent',
                [str(self.pk), self.first_name, self.last_name, self.email]
            )
        else:
            response = invoke_chaincode(
                client,
                user,
                'student_cc',
                'CreateStudent',
                [str(self.pk), self.first_name, self.last_name, self.email]
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
            'student_cc',
            'UpdateStudent',
            [str(self.pk), self.first_name, self.last_name, self.email, 'true']
        )
        return response

    @classmethod
    def all(cls):
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
            'student_cc',
            'GetAllStudents',
            []
        )

        students = json.loads(response)['students']
        students_res = []
        for student in students:
            students_res.append(cls(first_name=student['first_name'], last_name=student['last_name'],
                                    email=student['email']))
        return students_res

    @classmethod
    def get_student(cls, student_id):
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
            'student_cc',
            'QueryStudent',
            [student_id]
        )

        student = json.loads(response)
        student = cls(first_name=student['first_name'], last_name=student['last_name'], email=student['email'])
        return student

    @classmethod
    def get_students_by_title(cls, title_id):
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
            'student_cc',
            'GetStudentsByTitle',
            [title_id]
        )

        students = json.loads(response)['students']
        students_res = []
        for student in students:
            students_res.append(cls(first_name=student['first_name'], last_name=student['last_name'],
                                    email=student['email']))
        return students_res

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
            'student_cc',
            'GetStudentsByCourse',
            [course_id]
        )

        students = json.loads(response)['students']
        students_res = []
        for student in students:
            students_res.append(cls(first_name=student['first_name'], last_name=student['last_name'],
                                    email=student['email']))
        return students_res

    @classmethod
    def enroll_student_in_course(cls, students_id, course_id):
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
            'student_cc',
            'EnrollStudentsInCourse',
            [students_id, course_id]
        )

        return response

    @classmethod
    def de_enroll_student_in_course(cls, students_id, courses_id):
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
            'student_cc',
            'DeEnrollStudentsInCourse',
            [students_id, courses_id]
        )

        return response
