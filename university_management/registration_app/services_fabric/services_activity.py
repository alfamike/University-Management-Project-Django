import asyncio
import json
import uuid

from django.db import models

from registration_app.services_fabric.services_course import Course
from registration_app.services_fabric.services_fabric import HyperledgeFabric


class Activity(models.Model):
    """
    Model representing an Activity in the system.

    Attributes:
        id (UUIDField): The primary key for the activity, generated automatically.
        course (ForeignKey): A foreign key to the Course model.
        name (CharField): The name of the activity.
        description (TextField): A description of the activity, optional.
        due_date (DateField): The due date of the activity.
        is_deleted (BooleanField): A flag indicating if the activity is deleted, defaults to False.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, related_name='activities', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        """
        Return the string representation of the activity, which includes its name and course.
        """
        return f"{self.name} ({self.course})"

    def save(self, *args, **kwargs):
        """
        Save the activity to the database and invoke the appropriate chaincode function
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
        """
        Delete the activity from the database and invoke the deleteActivity chaincode function
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
            'activity_cc',
            'UpdateActivity',
            [str(self.pk), str(self.course.primary_key), self.name, self.description or '', str(self.due_date), 'true']
        ))
        return response

    @classmethod
    def all(cls):
        """
        Retrieve all activities from the Hyperledger Fabric network.

        Returns:
            list: A list of Activity instances.
        """
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
        """
        Retrieve a specific activity by its ID from the Hyperledger Fabric network.

        Args:
            activity_id (str): The ID of the activity to retrieve.

        Returns:
            Activity: An instance of the Activity class.
        """
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
        """
        Retrieve all activities for a specific course from the Hyperledger Fabric network.

        Args:
            course_id (str): The ID of the course.

        Returns:
            list: A list of Activity instances.
        """
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