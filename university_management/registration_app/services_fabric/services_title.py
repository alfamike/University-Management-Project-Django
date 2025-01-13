import json
import uuid

from django.db import models

from registration_app.services_fabric.services_fabric import query_chaincode, invoke_chaincode, \
    FabricClientSingleton


class Title(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        fabric_client_singleton = FabricClientSingleton.get_instance()
        client = fabric_client_singleton.get_client()
        user = fabric_client_singleton.get_user()

        existing_title = Title.get_title(str(self.pk))

        if existing_title is not None:
            response = invoke_chaincode(
                client,
                user,
                chaincode_name='title_cc',
                function='updateTitle',
                args=[self.pk, self.name, self.description or '']
            )
        else:
            response = invoke_chaincode(
                client,
                chaincode_name='title_cc',
                function='createTitle',
                args=[self.pk, self.name, self.description or '']
            )
        return response

    def delete(self, *args, **kwargs):

        fabric_client_singleton = FabricClientSingleton()
        client = fabric_client_singleton.get_client()
        user = fabric_client_singleton.get_user()

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

        fabric_client_singleton = FabricClientSingleton()
        client = fabric_client_singleton.get_client()
        user = fabric_client_singleton.get_user()

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

        fabric_client_singleton = FabricClientSingleton()
        client = fabric_client_singleton.get_client()
        user = fabric_client_singleton.get_user()

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
