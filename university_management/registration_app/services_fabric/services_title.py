import asyncio
import json
import os
import uuid

from django.db import models
from hfc.fabric import Client

from registration_app.services_fabric.services_fabric import query_chaincode, invoke_chaincode


class Title(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        print("Entering save method of Title...")
        connection_profile_path = os.path.join(
            os.path.dirname(__file__),
            'connection-profile.json'
        )

        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        client = Client(net_profile=connection_profile_path)

        try:
            user = client.get_user(org_name='Org1', name='Admin')
            print("Fabric user retrieved successfully.")
        except ValueError as e:
            print(f"Error retrieving Fabric user: {e}")
            raise

        existing_title = Title.get_title(str(self.pk))

        if existing_title is not None:
            response = loop.run_until_complete(invoke_chaincode(
                client,
                user,
                chaincode_name='title_cc',
                function='updateTitle',
                args=[self.pk, self.name, self.description or '']
            ))
        else:
            response = loop.run_until_complete(invoke_chaincode(
                client,
                user,
                chaincode_name='title_cc',
                function='createTitle',
                args=[self.pk, self.name, self.description or '']
            ))
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
            chaincode_name='title_cc',
            function='deleteTitle',
            args=[self.pk]
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
            chaincode_name='title_cc',
            function='queryAllTitles',
            args=[]
        )

        titles = json.loads(response)['titles']
        titles_res = []
        for title in titles:
            titles_res.append(cls(name=title['name'], description=title['description']))

        return titles_res

    @classmethod
    def get_title(cls, title_id):

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
            chaincode_name='title_cc',
            function='QueryTitle',
            args=[title_id]
        )

        title = json.loads(response)
        title = cls(name=title['name'], description=title['description'])

        return title
