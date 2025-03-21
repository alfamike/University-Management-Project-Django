import asyncio
import json
import uuid

from django.db import models

from registration_app.services_fabric.services_fabric import HyperledgeFabric
from registration_app.services_fabric.services_title import Title


class Course(models.Model):
    """
    Model representing a Course in the system.

    Attributes:
        id (UUIDField): The primary key for the course, generated automatically.
        title (ForeignKey): A foreign key to the Title model.
        name (CharField): The name of the course.
        description (TextField): A description of the course, optional.
        start_date (DateField): The start date of the course.
        end_date (DateField): The end date of the course.
        is_deleted (BooleanField): A flag indicating if the course is deleted, defaults to False.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.ForeignKey(Title, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        """
        Return the string representation of the course, which includes its name and title.
        """
        return f"{self.name} ({self.title})"

    def save(self, *args, **kwargs):
        """
        Save the course to the database and invoke the appropriate chaincode function
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
                      str(self.start_date), str(self.end_date)]
            ))
        return response

    def delete(self, *args, **kwargs):
        """
        Delete the course from the database and invoke the deleteCourse chaincode function
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
            chaincode_name='course_cc',
            function='UpdateCourse',
            args=[str(self.pk), str(self.title.primary_key), self.name, self.description or '', str(self.start_date),
                  str(self.end_date), 'true']
        ))
        return response

    @classmethod
    def all(cls):
        """
        Retrieve all courses from the Hyperledger Fabric network.

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
        """
        Retrieve a specific course by its ID from the Hyperledger Fabric network.

        Args:
            course_id (str): The ID of the course to retrieve.

        Returns:
            Course: An instance of the Course class.
        """
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
        """
        Retrieve all courses for a specific title and year from the Hyperledger Fabric network.

        Args:
            title_id (str): The ID of the title.
            year (str): The year to filter courses by.

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
