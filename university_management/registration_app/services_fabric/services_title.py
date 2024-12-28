import json

from django.db import models

from registration_app.services_fabric.services_fabric import query_chaincode, get_fabric_client, invoke_chaincode


class Title(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        client = get_fabric_client()

        existing_title = Title.get_title(str(self.pk))

        if existing_title is not None:
            response = invoke_chaincode(
                client,
                chaincode_name='title_cc',
                function='UpdateTitle',
                args=[str(self.pk), self.name, self.description or '']
            )
        else:
            response = invoke_chaincode(
                client,
                chaincode_name='title_cc',
                function='CreateTitle',
                args=[str(self.pk), self.name, self.description or '']
            )
        return response

    def delete(self, *args, **kwargs):

        client = get_fabric_client()

        response = invoke_chaincode(
            client,
            chaincode_name='title_cc',
            function='UpdateTitle',
            args=[str(self.pk), self.name, self.description or '', 'true']
        )
        return response

    @classmethod
    def all(cls):

        client = get_fabric_client()

        response = query_chaincode(
            client,
            chaincode_name='title_cc',
            function='GetAllTitles',
            args=[]
        )

        titles = json.loads(response)['titles']
        titles_res = []
        for title in titles:
            titles_res.append(cls(name=title['name'], description=title['description']))

        return titles_res

    @classmethod
    def get_title(cls, title_id):

        client = get_fabric_client()

        response = query_chaincode(
            client,
            chaincode_name='title_cc',
            function='QueryTitle',
            args=[title_id]
        )

        title = json.loads(response)
        title = cls(name=title['name'], description=title['description'])

        return title
