import asyncio
import json
import uuid

from django.db import models

from registration_app.services_fabric.services_fabric import HyperledgeFabric


class Student(models.Model):
    """
    Model representing a Student in the system.

    Attributes:
        id (UUIDField): The primary key for the student, generated automatically.
        first_name (CharField): The first name of the student.
        last_name (CharField): The last name of the student.
        email (EmailField): The email of the student, must be unique.
        is_deleted (BooleanField): A flag indicating if the student is deleted, defaults to False.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        """
        Return the string representation of the student, which is their full name.
        """
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        """
        Save the student to the database and invoke the appropriate chaincode function
        on the Hyperledger Fabric network.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The response from the Hyperledger Fabric network.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        existing_student = Student.get_student(str(self.pk))

        if existing_student is not None:
            response = loop.run_until_complete(HyperledgeFabric.invoke_chaincode(
                'student_cc',
                'UpdateStudent',
                [str(self.pk), self.first_name, self.last_name, self.email]
            ))
        else:
            response = loop.run_until_complete(HyperledgeFabric.invoke_chaincode(
                'student_cc',
                'CreateStudent',
                [str(self.pk), self.first_name, self.last_name, self.email]
            ))
        return response

    def delete(self, *args, **kwargs):
        """
        Delete the student from the database and invoke the deleteStudent chaincode function
        on the Hyperledger Fabric network.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The response from the Hyperledger Fabric network.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.invoke_chaincode(
            'student_cc',
            'UpdateStudent',
            [str(self.pk), self.first_name, self.last_name, self.email, 'true']
        ))
        return response

    @classmethod
    def all(cls):
        """
        Retrieve all students from the Hyperledger Fabric network.

        Returns:
            list: A list of Student instances.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            'student_cc',
            'GetAllStudents',
            []
        ))

        students = json.loads(response)['students']
        students_res = []
        for student in students:
            students_res.append(cls(first_name=student['first_name'], last_name=student['last_name'],
                                    email=student['email']))
        return students_res

    @classmethod
    def get_student(cls, student_id):
        """
        Retrieve a specific student by their ID from the Hyperledger Fabric network.

        Args:
            student_id (str): The ID of the student to retrieve.

        Returns:
            Student: An instance of the Student class.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            'student_cc',
            'QueryStudent',
            [student_id]
        ))

        student = json.loads(response)
        student = cls(first_name=student['first_name'], last_name=student['last_name'], email=student['email'])
        return student

    @classmethod
    def get_students_by_title(cls, title_id):
        """
        Retrieve all students associated with a specific title from the Hyperledger Fabric network.

        Args:
            title_id (str): The ID of the title.

        Returns:
            list: A list of Student instances.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            'student_cc',
            'GetStudentsByTitle',
            [title_id]
        ))

        students = json.loads(response)['students']
        students_res = []
        for student in students:
            students_res.append(cls(first_name=student['first_name'], last_name=student['last_name'],
                                    email=student['email']))
        return students_res

    @classmethod
    def get_students_by_course(cls, course_id):
        """
        Retrieve all students associated with a specific course from the Hyperledger Fabric network.

        Args:
            course_id (str): The ID of the course.

        Returns:
            list: A list of Student instances.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            'student_cc',
            'GetStudentsByCourse',
            [course_id]
        ))

        students = json.loads(response)['students']
        students_res = []
        for student in students:
            students_res.append(cls(first_name=student['first_name'], last_name=student['last_name'],
                                    email=student['email']))
        return students_res

    @classmethod
    def enroll_student_in_course(cls, students_id, course_id):
        """
        Enroll a student in a specific course on the Hyperledger Fabric network.

        Args:
            students_id (str): The ID of the student.
            course_id (str): The ID of the course.

        Returns:
            The response from the Hyperledger Fabric network.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.invoke_chaincode(
            'student_cc',
            'EnrollStudentsInCourse',
            [students_id, course_id]
        ))

        return response

    @classmethod
    def de_enroll_student_in_course(cls, students_id, courses_id):
        """
        De-enroll a student from a specific course on the Hyperledger Fabric network.

        Args:
            students_id (str): The ID of the student.
            courses_id (str): The ID of the course.

        Returns:
            The response from the Hyperledger Fabric network.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.invoke_chaincode(
            'student_cc',
            'DeEnrollStudentsInCourse',
            [students_id, courses_id]
        ))

        return response