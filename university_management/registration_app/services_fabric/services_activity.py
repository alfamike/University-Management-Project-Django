import asyncio
import json
import os
import uuid

from django.db import models
from hfc.fabric import Client

from registration_app.services_fabric.services_course import Course
from registration_app.services_fabric.services_fabric import HyperledgeFabric


class Activity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, related_name='activities', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.course})"

    def save(self, *args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        existing_activity = Activity.get_activity(str(self.pk))

        if existing_activity is not None:
            response = loop.run_until_complete(HyperledgeFabric.invoke_chaincode(
                'activity_cc',
                'UpdateActivity',
                [str(self.pk), str(self.course.primary_key), self.name, self.description or '', str(self.due_date)]
            ))
        else:
            response = loop.run_until_complete(HyperledgeFabric.invoke_chaincode(
                'activity_cc',
                'CreateActivity',
                [str(self.pk), str(self.course.primary_key), self.name, self.description or '', str(self.due_date)]
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
            'activity_cc',
            'UpdateActivity',
            [str(self.pk), str(self.course.primary_key), self.name, self.description or '', str(self.due_date), 'true']
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
            'activity_cc',
            'GetAllActivities',
            []
        ))

        activities = json.loads(response)['activities']
        activities_res = []
        for activity in activities:
            activities_res.append(cls(name=activity['name'], description=activity['description'],
                                      due_date=activity['due_date'], course=Course.get_course(activity['course_id'])))

        return activities_res

    @classmethod
    def get_activity(cls, activity_id):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            'activity_cc',
            'QueryActivity',
            [activity_id]
        ))

        activity = json.loads(response)
        activity = cls(name=activity['name'], description=activity['description'], due_date=activity['due_date'],
                       course=Course.get_course(activity['course_id']))

        return activity

    @classmethod
    def get_activities_by_course(cls, course_id):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            'activity_cc',
            'GetActivitiesByCourse',
            [course_id]
        ))

        activities = json.loads(response)['activities']
        activities_res = []
        for activity in activities:
            activities_res.append(cls(name=activity['name'], description=activity['description'],
                                      due_date=activity['due_date'], course=Course.get_course(activity['course_id'])))

        return activities_res
