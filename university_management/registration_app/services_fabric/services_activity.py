import json
import os
import uuid

from django.db import models
from hfc.fabric import Client

from registration_app.services_fabric.services_course import Course
from registration_app.services_fabric.services_fabric import query_chaincode, invoke_chaincode


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

        existing_activity = Activity.get_activity(str(self.pk))

        if existing_activity is not None:
            response = invoke_chaincode(
                client,
                user,
                'activity_cc',
                'UpdateActivity',
                [str(self.pk), str(self.course.primary_key), self.name, self.description or '', str(self.due_date)]
            )
        else:
            response = invoke_chaincode(
                client,
                user,
                'activity_cc',
                'CreateActivity',
                [str(self.pk), str(self.course.primary_key), self.name, self.description or '', str(self.due_date)]
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
            'activity_cc',
            'UpdateActivity',
            [str(self.pk), str(self.course.primary_key), self.name, self.description or '', str(self.due_date), 'true']
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
            'activity_cc',
            'GetAllActivities',
            []
        )

        activities = json.loads(response)['activities']
        activities_res = []
        for activity in activities:
            activities_res.append(cls(name=activity['name'], description=activity['description'],
                                      due_date=activity['due_date'], course=Course.get_course(activity['course_id'])))

        return activities_res

    @classmethod
    def get_activity(cls, activity_id):
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
            'activity_cc',
            'QueryActivity',
            [activity_id]
        )

        activity = json.loads(response)
        activity = cls(name=activity['name'], description=activity['description'], due_date=activity['due_date'],
                       course=Course.get_course(activity['course_id']))

        return activity

    @classmethod
    def get_activities_by_course(cls, course_id):
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
            'activity_cc',
            'GetActivitiesByCourse',
            [course_id]
        )

        activities = json.loads(response)['activities']
        activities_res = []
        for activity in activities:
            activities_res.append(cls(name=activity['name'], description=activity['description'],
                                      due_date=activity['due_date'], course=Course.get_course(activity['course_id'])))

        return activities_res
