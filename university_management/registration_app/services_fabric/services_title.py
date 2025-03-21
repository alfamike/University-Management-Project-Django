import asyncio
import json
import uuid

from django.db import models

from registration_app.services_fabric.services_fabric import HyperledgeFabric


class Title(models.Model):
    """
    Model representing a Title in the system.

    Attributes:
        id (UUIDField): The primary key for the title, generated automatically.
        name (CharField): The name of the title, must be unique.
        description (TextField): A description of the title, optional.
        is_deleted (BooleanField): A flag indicating if the title is deleted, defaults to False.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        """
        Return the string representation of the title, which is its name.
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Save the title to the database and invoke the appropriate chaincode function
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

        existing_title = Title.get_title(str(self.pk))

        if existing_title is not None:
            response = loop.run_until_complete(HyperledgeFabric.invoke_chaincode(
                chaincode_name='title_cc',
                function='updateTitle',
                args=[self.pk, self.name, self.description or '']
            ))
        else:
            response = loop.run_until_complete(HyperledgeFabric.invoke_chaincode(
                chaincode_name='title_cc',
                function='createTitle',
                args=[self.pk, self.name, self.description or '']
            ))
        return response

    def delete(self, *args, **kwargs):
        """
        Delete the title from the database and invoke the deleteTitle chaincode function
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
            chaincode_name='title_cc',
            function='deleteTitle',
            args=[self.pk]
        ))
        return response

    @classmethod
    def all(cls):
        """
        Retrieve all titles from the Hyperledger Fabric network.

        Returns:
            list: A list of Title instances.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        response = loop.run_until_complete(HyperledgeFabric.query_chaincode(
            chaincode_name='title_cc',
            function='queryAllTitles',
            args=[]
        ))

        titles = json.loads(response)['titles']
        titles_res = []
        for title in titles:
            titles_res.append(cls(name=title['name'], description=title['description']))

        return titles_res

    @classmethod
    def get_title(cls, title_id):
        """
        Retrieve a specific title by its ID from the Hyperledger Fabric network.

        Args:
            title_id (str): The ID of the title to retrieve.

        Returns:
            Title: An instance of the Title class.
        """
        response = HyperledgeFabric.query_chaincode(
            chaincode_name='title_cc',
            function='queryTitle',
            args=[title_id]
        )

        title = json.loads(response)
        title = cls(name=title['name'], description=title['description'])

        return title