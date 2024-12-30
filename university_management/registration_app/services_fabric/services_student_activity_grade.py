import json
import uuid

from django.db import models

from registration_app.services_fabric.services_activity import Activity
from registration_app.services_fabric.services_fabric import query_chaincode, get_fabric_client, invoke_chaincode
from registration_app.services_fabric.services_student import Student


class StudentActivityGrade(models.Model):
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
        return f"{self.student} - {self.activity}: {self.grade}"

    def save(self, *args, **kwargs):
        client = get_fabric_client()

        existing_student_activity_grade = (StudentActivityGrade.
                                           get_student_activity_grade_by_params(str(self.student.primary_key),
                                                                                str(self.activity.primary_key)))

        if existing_student_activity_grade is not None:
            response = invoke_chaincode(
                client,
                'student_activity_grade_cc',
                'UpdateStudentActivityGrade',
                [str(self.pk), str(self.student.primary_key), str(self.activity.primary_key), str(self.grade)]
            )
        else:
            response = invoke_chaincode(
                client,
                'student_activity_grade_cc',
                'CreateStudentActivityGrade',
                [str(self.pk), str(self.student.primary_key), str(self.activity.primary_key), str(self.grade)]
            )
        return response

    def delete(self, *args, **kwargs):
        client = get_fabric_client()

        response = invoke_chaincode(
            client,
            'student_activity_grade_cc',
            'UpdateStudentActivityGrade',
            [str(self.pk), str(self.student.primary_key), str(self.activity.primary_key), 'true']
        )
        return response

    @classmethod
    def all(cls):
        client = get_fabric_client()
        response = query_chaincode(client, 'student_activity_grade_cc', 'GetAllStudentActivityGrades', [])

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
        client = get_fabric_client()
        response = query_chaincode(
            client,
            'student_activity_grade_cc',
            'GetStudentActivityGrade',
            [student_activity_grade_id]
        )

        student_activity_grade = json.loads(response)
        student_activity_grade = cls(student=Student.get_student(student_activity_grade['student_id']),
                                     activity=Activity.get_activity(student_activity_grade['activity_id']),
                                     grade=student_activity_grade['grade'])
        return student_activity_grade

    @classmethod
    def get_student_activity_grade_by_params(cls, student_id, activity_id):
        client = get_fabric_client()
        response = query_chaincode(
            client,
            'student_activity_grade_cc',
            'GetStudentActivityGradeByParams',
            [student_id, activity_id]
        )

        student_activity_grade = json.loads(response)
        student_activity_grade = cls(student=Student.get_student(student_activity_grade['student_id']),
                                     activity=Activity.get_activity(student_activity_grade['activity_id']),
                                     grade=student_activity_grade['grade'])
        return student_activity_grade

    @classmethod
    def get_student_activity_grades(cls, student_id):
        client = get_fabric_client()

        response = query_chaincode(
            client,
            'student_activity_grade_cc',
            'GetStudentActivityGrades',
            [student_id]
        )

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
        client = get_fabric_client()

        response = query_chaincode(
            client,
            'student_activity_grade_cc',
            'GetActivityStudentGrades',
            [activity_id]
        )

        activity_student_grades = json.loads(response)['activity_student_grades']
        activity_student_grades_res = []
        for activity_student_grade in activity_student_grades:
            activity_student_grades_res.append(cls(
                student=Student.get_student(activity_student_grade['student_id']),
                activity=Activity.get_activity(activity_student_grade['activity_id']),
                grade=activity_student_grade['grade']
            ))
        return activity_student_grades_res
