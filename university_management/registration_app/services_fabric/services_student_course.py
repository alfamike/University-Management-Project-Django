import asyncio
import json
import uuid

from django.db import models

from registration_app.services_fabric.services_course import Course
from registration_app.services_fabric.services_fabric import HyperledgeFabric
from registration_app.services_fabric.services_student import Student


class StudentCourse(models.Model):
    """
    Model representing the relationship between a student and a course, including the grade.

    Attributes:
        id (UUIDField): The primary key for the student-course relationship, generated automatically.
        student (ForeignKey): A foreign key to the Student model.
        course (ForeignKey): A foreign key to the Course model.
        grade (DecimalField): The grade of the student in the course.
        is_deleted (BooleanField): A flag indicating if the relationship is deleted, defaults to False.
    """
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
        """
        Return the string representation of the student-course relationship.
        """
        return f"{self.student} - {self.course}"

    def save(self, *args, **kwargs):
        """
        Save the student-course relationship to the database and invoke the appropriate chaincode function
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
        """
        Delete the student-course relationship from the database and invoke the deleteStudentCourse chaincode function
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
            'student_course_cc',
            'UpdateStudentCourse',
            [str(self.pk), str(self.student.primary_key), str(self.course.primary_key), self.grade,
             'true']
        ))
        return response

    @classmethod
    def all(cls):
        """
        Retrieve all student-course relationships from the Hyperledger Fabric network.

        Returns:
            list: A list of StudentCourse instances.
        """
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
        """
        Retrieve all courses for a specific student from the Hyperledger Fabric network.

        Args:
            student_id (str): The ID of the student.

        Returns:
            list: A list of Course instances.
        """
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
        """
        Retrieve all students for a specific course from the Hyperledger Fabric network.

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
        """
        Retrieve a specific student-course relationship by its ID from the Hyperledger Fabric network.

        Args:
            student_course_id (str): The ID of the student-course relationship.

        Returns:
            StudentCourse: An instance of the StudentCourse class.
        """
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
        """
        Retrieve a specific student-course relationship by student ID and course ID from the Hyperledger Fabric network.

        Args:
            student_id (str): The ID of the student.
            course_id (str): The ID of the course.

        Returns:
            StudentCourse: An instance of the StudentCourse class.
        """
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