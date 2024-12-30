import json
import uuid

from django.db import models

from registration_app.services_fabric.services_course import Course
from registration_app.services_fabric.services_fabric import query_chaincode, get_fabric_client, invoke_chaincode
from registration_app.services_fabric.services_student import Student


class StudentCourseGrade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, related_name='course_grades', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='student_grades', on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_student_course')
        ]

    def __str__(self):
        return f"{self.student} - {self.course}: {self.grade}"

    def save(self, *args, **kwargs):
        client = get_fabric_client()

        existing_student_course_grade = (
            StudentCourseGrade.get_student_course_grade_by_params(
                str(self.student.primary_key), str(self.course.primary_key)))

        if existing_student_course_grade is not None:
            response = invoke_chaincode(
                client,
                'student_course_grade_cc',
                'UpdateStudentCourseGrade',
                [str(self.pk), str(self.student.primary_key), str(self.course.primary_key), str(self.grade)]
            )
        else:
            response = invoke_chaincode(
                client,
                'student_course_grade_cc',
                'CreateStudentCourseGrade',
                [str(self.pk), str(self.student.primary_key), str(self.course.primary_key), str(self.grade)]
            )
        return response

    def delete(self, *args, **kwargs):
        client = get_fabric_client()

        response = invoke_chaincode(
            client,
            'student_course_grade_cc',
            'UpdateStudentCourseGrade',
            [str(self.pk), str(self.student.primary_key), str(self.course.primary_key), 'true']
        )
        return response

    @classmethod
    def get_student_course_grade(cls, student_course_grade_id):
        client = get_fabric_client()
        response = query_chaincode(
            client,
            'student_course_grade_cc',
            'GetStudentCourseGrade',
            [student_course_grade_id]
        )
        return response

    @classmethod
    def get_student_course_grade_by_params(cls, student_id, course_id):
        client = get_fabric_client()
        response = query_chaincode(
            client,
            'student_course_grade_cc',
            'GetStudentCourseGradeByParams',
            [student_id, course_id]
        )
        return response

    @classmethod
    def all(cls):
        client = get_fabric_client()
        response = query_chaincode(client, 'student_course_grade_cc', 'GetAllStudentCourseGrades', [])

        student_course_grades = json.loads(response)['student_course_grades']
        student_course_grades_res = []
        for student_course_grade in student_course_grades:
            student_course_grades_res.append(cls(student=Student.get_student(student_course_grade['student_id']),
                                                 course=Course.get_course(student_course_grade['course_id']),
                                                 grade=student_course_grade['grade']))
        return student_course_grades_res

    @classmethod
    def get_student_course_grades(cls, student_id):
        client = get_fabric_client()
        response = query_chaincode(
            client,
            'student_course_grade_cc',
            'GetStudentCourseGrades',
            [student_id]
        )
        student_course_grades = json.loads(response)['student_course_grades']
        student_course_grades_res = []
        for student_course_grade in student_course_grades:
            student_course_grades_res.append(cls(student=Student.get_student(student_course_grade['student_id']),
                                                 course=Course.get_course(student_course_grade['course_id']),
                                                 grade=student_course_grade['grade']))
        return student_course_grades_res

    @classmethod
    def get_course_student_grades(cls, course_id):
        client = get_fabric_client()
        response = query_chaincode(
            client,
            'student_course_grade_cc',
            'GetCourseStudentGrades',
            [course_id]
        )
        student_course_grades = json.loads(response)['student_course_grades']
        student_course_grades_res = []
        for student_course_grade in student_course_grades:
            student_course_grades_res.append(cls(student=Student.get_student(student_course_grade['student_id']),
                                                 course=Course.get_course(student_course_grade['course_id']),
                                                 grade=student_course_grade['grade']))
        return student_course_grades_res
