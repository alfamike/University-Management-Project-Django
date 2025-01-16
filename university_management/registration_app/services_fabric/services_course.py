import asyncio
import json
import os
import uuid

from django.db import models
from hfc.fabric import Client

from registration_app.services_fabric.services_fabric import HyperledgeFabric
from registration_app.services_fabric.services_title import Title


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.ForeignKey(Title, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.title})"

    def save(self, *args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        existing_course = Course.get_course(str(self.pk))

        if existing_course is not None:
            response = loop.run_until_complete(HyperledgeFabric.invoke_chaincode(
                chaincode_name='course_cc',
                function='UpdateCourse',
                args=[str(self.pk), str(self.title.primary_key), self.name, self.description or '',
                      str(self.start_date), str(self.end_date)]
            ))
        else:
            response = loop.run_until_complete(HyperledgeFabric.invoke_chaincode(
                chaincode_name='course_cc',
                function='CreateCourse',
                args=[str(self.pk), str(self.title.primary_key), self.name, self.description or '',
                      str(self.start_date),
                      str(self.end_date)]
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
            chaincode_name='course_cc',
            function='UpdateCourse',
            args=[str(self.pk), str(self.title.primary_key), self.name, self.description or '', str(self.start_date),
                  str(self.end_date), 'true']
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
            chaincode_name='course_cc',
            function='GetAllCourses',
            args=[]
        ))

        courses = json.loads(response)['courses']
        courses_res = []
        for course in courses:
            courses_res.append(cls(title=Title.get_title(course['title_id']), name=course['name'],
                               description=course['description'], start_date=course['start_date'],
                               end_date=course['end_date']))

        return courses_res

    @classmethod
    def get_course(cls, course_id):

        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            chaincode_name='course_cc',
            function='QueryCourse',
            args=[course_id]
        ))

        course = json.loads(response)
        course = cls(title=Title.get_title(course['title_id']), name=course['name'],
                     description=course['description'],
                     start_date=course['start_date'], end_date=course['end_date'])
        return course

    @classmethod
    def get_courses_by_title_year(cls, title_id, year):

        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            'course_cc',
            'GetCoursesByTitleYear',
            [title_id, year]
        ))

        courses = json.loads(response)['courses']
        courses_res = []
        for course in courses:
            courses_res.append(cls(title=Title.get_title(course['title_id']), name=course['name'],
                               description=course['description'], start_date=course['start_date'],
                               end_date=course['end_date']))

        return courses_res
