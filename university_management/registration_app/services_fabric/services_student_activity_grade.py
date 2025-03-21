import asyncio
import json
import uuid

from django.db import models

from registration_app.services_fabric.services_activity import Activity
from registration_app.services_fabric.services_fabric import HyperledgeFabric
from registration_app.services_fabric.services_student import Student


class StudentActivityGrade(models.Model):
    """
    Model representing the grade of a student for a specific activity.

    Attributes:
        id (UUIDField): The primary key for the student-activity grade, generated automatically.
        student (ForeignKey): A foreign key to the Student model.
        activity (ForeignKey): A foreign key to the Activity model.
        grade (DecimalField): The grade of the student in the activity.
        is_deleted (BooleanField): A flag indicating if the grade is deleted, defaults to False.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, related_name='activities_grades', on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, related_name='student_grades', on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'activity'], name='unique_student_activity_grade')
        ]

    def __str__(self):
        """
        Return the string representation of the student-activity grade.
        """
        return f"{self.student} - {self.activity}: {self.grade}"

    def save(self, *args, **kwargs):
        """
        Save the student-activity grade to the database and invoke the appropriate chaincode function
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

        existing_student_activity_grade = (StudentActivityGrade.
                                           get_student_activity_grade_by_params(str(self.student.primary_key),
                                                                                str(self.activity.primary_key)))

        if existing_student_activity_grade is not None:
            response = loop.run_until_complete(HyperledgeFabric.invoke_chaincode(
                'student_activity_grade_cc',
                'UpdateStudentActivityGrade',
                [str(self.pk), str(self.student.primary_key), str(self.activity.primary_key), str(self.grade)]
            ))
        else:
            response = loop.run_until_complete(HyperledgeFabric.invoke_chaincode(
                'student_activity_grade_cc',
                'CreateStudentActivityGrade',
                [str(self.pk), str(self.student.primary_key), str(self.activity.primary_key), str(self.grade)]
            ))
        return response

    def delete(self, *args, **kwargs):
        """
        Delete the student-activity grade from the database and invoke the deleteStudentActivityGrade chaincode function
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
            'student_activity_grade_cc',
            'UpdateStudentActivityGrade',
            [str(self.pk), str(self.student.primary_key), str(self.activity.primary_key), 'true']
        ))
        return response

    @classmethod
    def all(cls):
        """
        Retrieve all student-activity grades from the Hyperledger Fabric network.

        Returns:
            list: A list of StudentActivityGrade instances.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.
                                           query_chaincode('student_activity_grade_cc', 'GetAllStudentActivityGrades', []))

        student_activities_grades = json.loads(response)['student_activities_grades']
        student_activities_grades_res = []
        for student_activity_grade in student_activities_grades:
            student_activities_grades_res.append(cls(
                student=Student.get_student(student_activity_grade['student_id']),
                activity=Activity.get_activity(student_activity_grade['activity_id']),
                grade=student_activity_grade['grade']
            ))
        return student_activities_grades_res

    @classmethod
    def get_student_activity_grade(cls, student_activity_grade_id):
        """
        Retrieve a specific student-activity grade by its ID from the Hyperledger Fabric network.

        Args:
            student_activity_grade_id (str): The ID of the student-activity grade.

        Returns:
            StudentActivityGrade: An instance of the StudentActivityGrade class.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            'student_activity_grade_cc',
            'GetStudentActivityGrade',
            [student_activity_grade_id]
        ))

        student_activity_grade = json.loads(response)
        student_activity_grade = cls(student=Student.get_student(student_activity_grade['student_id']),
                                     activity=Activity.get_activity(student_activity_grade['activity_id']),
                                     grade=student_activity_grade['grade'])
        return student_activity_grade

    @classmethod
    def get_student_activity_grade_by_params(cls, student_id, activity_id):
        """
        Retrieve a specific student-activity grade by student ID and activity ID from the Hyperledger Fabric network.

        Args:
            student_id (str): The ID of the student.
            activity_id (str): The ID of the activity.

        Returns:
            StudentActivityGrade: An instance of the StudentActivityGrade class.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            'student_activity_grade_cc',
            'GetStudentActivityGradeByParams',
            [student_id, activity_id]
        ))

        student_activity_grade = json.loads(response)
        student_activity_grade = cls(student=Student.get_student(student_activity_grade['student_id']),
                                     activity=Activity.get_activity(student_activity_grade['activity_id']),
                                     grade=student_activity_grade['grade'])
        return student_activity_grade

    @classmethod
    def get_student_activity_grades(cls, student_id):
        """
        Retrieve all activity grades for a specific student from the Hyperledger Fabric network.

        Args:
            student_id (str): The ID of the student.

        Returns:
            list: A list of StudentActivityGrade instances.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            'student_activity_grade_cc',
            'GetStudentActivityGrades',
            [student_id]
        ))

        student_activity_grades = json.loads(response)['student_activity_grades']
        student_activities_grades_res = []
        for student_activity_grade in student_activity_grades:
            student_activities_grades_res.append(cls(
                student=Student.get_student(student_activity_grade['student_id']),
                activity=Activity.get_activity(student_activity_grade['activity_id']),
                grade=student_activity_grade['grade']
            ))
        return student_activities_grades_res

    @classmethod
    def get_activity_student_grades(cls, activity_id):
        """
        Retrieve all student grades for a specific activity from the Hyperledger Fabric network.

        Args:
            activity_id (str): The ID of the activity.

        Returns:
            list: A list of StudentActivityGrade instances.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            'student_activity_grade_cc',
            'GetActivityStudentGrades',
            [activity_id]
        ))

        activity_student_grades = json.loads(response)['activity_student_grades']
        activity_student_grades_res = []
        for activity_student_grade in activity_student_grades:
            activity_student_grades_res.append(cls(
                student=Student.get_student(activity_student_grade['student_id']),
                activity=Activity.get_activity(activity_student_grade['activity_id']),
                grade=activity_student_grade['grade']
            ))
        return activity_student_grades_res