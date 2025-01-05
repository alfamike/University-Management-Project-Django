import json
import uuid

from django.db import models

from registration_app.services_fabric.services_course import Course
from registration_app.services_fabric.services_fabric import query_chaincode, invoke_chaincode, \
    FabricClientSingleton


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
        fabric_client_singleton = FabricClientSingleton()
        client = fabric_client_singleton.get_client()
        user = fabric_client_singleton.get_user()

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
        fabric_client_singleton = FabricClientSingleton()
        client = fabric_client_singleton.get_client()
        user = fabric_client_singleton.get_user()

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
        fabric_client_singleton = FabricClientSingleton()
        client = fabric_client_singleton.get_client()
        user = fabric_client_singleton.get_user()

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
        fabric_client_singleton = FabricClientSingleton()
        client = fabric_client_singleton.get_client()
        user = fabric_client_singleton.get_user()

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
        fabric_client_singleton = FabricClientSingleton()
        client = fabric_client_singleton.get_client()
        user = fabric_client_singleton.get_user()

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
