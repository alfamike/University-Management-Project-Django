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
from registration_app.services_fabric.services_title import Title


class Course(models.Model):
    title = models.ForeignKey(Title, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.title})"

    def save(self, *args, **kwargs):

        client = get_fabric_client()

        existing_course = Course.get_course(str(self.pk))

        if existing_course is not None:
            response = invoke_chaincode(
                client,
                chaincode_name='course_cc',
                function='UpdateCourse',
                args=[str(self.pk), str(self.title.primary_key), self.name, self.description or '',
                      str(self.start_date), str(self.end_date)]
            )
        else:
            response = invoke_chaincode(
                client,
                chaincode_name='course_cc',
                function='CreateCourse',
                args=[str(self.pk), str(self.title.pk), self.name, self.description or '', str(self.start_date),
                      str(self.end_date)]
            )
        return response

    def delete(self, *args, **kwargs):

        client = get_fabric_client()

        response = invoke_chaincode(
            client,
            chaincode_name='course_cc',
            function='UpdateCourse',
            args=[str(self.pk), str(self.title.primary_key), self.name, self.description or '', str(self.start_date),
                  str(self.end_date), 'true']
        )
        return response

    @classmethod
    def all(cls):

        client = get_fabric_client()

        response = query_chaincode(
            client,
            chaincode_name='course_cc',
            function='GetAllCourses',
            args=[]
        )

        courses = json.loads(response)['courses']
        courses_res = []
        for course in courses:
            courses_res.append(cls(title=Title.get_title(course['title_id']), name=course['name'],
                               description=course['description'], start_date=course['start_date'],
                               end_date=course['end_date']))

        return courses_res

    @classmethod
    def get_course(cls, course_id):

        client = get_fabric_client()

        response = query_chaincode(
            client,
            chaincode_name='course_cc',
            function='QueryCourse',
            args=[course_id]
        )

        course = json.loads(response)
        course = cls(title=Title.get_title(course['title_id']), name=course['name'],
                     description=course['description'],
                     start_date=course['start_date'], end_date=course['end_date'])
        return course

    @classmethod
    def get_courses_by_title_year(cls, year):

        client = get_fabric_client()

        response = query_chaincode(
            client,
            'course_cc',
            'GetCoursesByTitleYear',
            [year]
        )

        courses = json.loads(response)['courses']
        courses_res = []
        for course in courses:
            courses_res.append(cls(title=Title.get_title(course['title_id']), name=course['name'],
                               description=course['description'], start_date=course['start_date'],
                               end_date=course['end_date']))

        return courses_res
