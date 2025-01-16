import asyncio
import json
import os
import uuid
from hfc.fabric_network import wallet
from django.db import models
from hfc.fabric import Client

from registration_app.services_fabric.services_fabric import HyperledgeFabric


class Title(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
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

        response = HyperledgeFabric.query_chaincode(
            chaincode_name='title_cc',
            function='QueryTitle',
            args=[title_id]
        )

        title = json.loads(response)
        title = cls(name=title['name'], description=title['description'])

        return title
